"""
Processor Orchestrator

Listens to Pub/Sub events and orchestrates processor execution for underwritings.
Handles both underwriting.created and underwriting.documents.updated events.
"""

import json
import logging
from typing import Dict, List, Any
from concurrent.futures import ProcessPoolExecutor, as_completed
from google.cloud import pubsub_v1

from processing_engine.models.execution import ProcessorInput, ProcessingResult
from processing_engine.processors.base_processor import BaseProcessor


class ProcessorOrchestrator:
    """
    Orchestrates processor execution based on Pub/Sub events.

    Listens to:
    - underwriting.created
    - underwriting.documents.updated

    Emits:
    - underwriting.processing.completed
    """

    def __init__(
        self,
        processor_registry,
        document_service,
        pubsub_publisher,
        project_id: str,
        topic_name: str = "underwriting.processing.completed"
    ):
        self.processor_registry = processor_registry
        self.document_service = document_service
        self.pubsub_publisher = pubsub_publisher
        self.project_id = project_id
        self.topic_name = topic_name
        self.logger = logging.getLogger(__name__)

        # Pub/Sub topic for completion events
        self.completion_topic = f"projects/{project_id}/topics/{topic_name}"

    def handle_underwriting_created(self, message_data: Dict[str, Any]) -> None:
        """Handle underwriting.created event."""
        self.logger.info(f"Processing underwriting.created event: {message_data}")

        account_id = message_data["account_id"]
        underwriting_id = message_data["underwriting_id"]
        documents = message_data["documents"]

        self._execute_processors(underwriting_id, account_id, documents)

    def handle_documents_updated(self, message_data: Dict[str, Any]) -> None:
        """Handle underwriting.documents.updated event."""
        self.logger.info(f"Processing underwriting.documents.updated event: {message_data}")

        account_id = message_data["account_id"]
        underwriting_id = message_data["underwriting_id"]
        documents = message_data["documents"]

        self._execute_processors(underwriting_id, account_id, documents)

    def _execute_processors(
        self,
        underwriting_id: str,
        account_id: str,
        documents: Dict[str, List[str]]
    ) -> None:
        """Execute all purchased processors for an underwriting."""

        # Get all purchased processors for this account
        processors = self.processor_registry.get_processors(account_id)

        if not processors:
            self.logger.warning(f"No processors found for account {account_id}")
            return

        # Convert documents to processor inputs
        processor_inputs = self._convert_documents_to_inputs(
            documents, account_id, underwriting_id
        )

        # Execute processors in parallel
        results = self._execute_processors_parallel(processors, processor_inputs)

        # Emit completion event
        self._emit_completion_event(underwriting_id, account_id, results)

    def _convert_documents_to_inputs(
        self,
        documents: Dict[str, List[str]],
        account_id: str,
        underwriting_id: str
    ) -> List[ProcessorInput]:
        """Convert documents dict to list of ProcessorInput objects."""
        inputs = []

        for document_type, document_ids in documents.items():
            for doc_id in document_ids:
                # Get document content from document service
                doc_content = self.document_service.get_document_content(doc_id)

                inputs.append(ProcessorInput(
                    input_id=doc_id,
                    account_id=account_id,
                    underwriting_id=underwriting_id,
                    data={
                        "document_type": document_type,
                        "document_id": doc_id,
                        "content": doc_content
                    }
                ))

        return inputs

    def _execute_processors_parallel(
        self,
        processors: List[BaseProcessor],
        inputs: List[ProcessorInput]
    ) -> List[Dict[str, Any]]:
        """Execute all processors in parallel using multiple processes."""
        results = []

        with ProcessPoolExecutor(max_workers=len(processors)) as executor:
            # Submit all processor execution tasks
            future_to_processor = {
                executor.submit(self._execute_single_processor, processor, inputs): processor
                for processor in processors
            }

            # Collect results as they complete
            for future in as_completed(future_to_processor):
                processor = future_to_processor[future]
                try:
                    result = future.result()
                    results.append({
                        "processor_name": processor.PROCESSOR_NAME,
                        "execution_id": result.execution_id,
                        "status": "completed" if result.success else "failed",
                        "factors": result.output if result.success else None,
                        "error": result.error if not result.success else None,
                        "execution_time": result.duration
                    })
                except Exception as e:
                    self.logger.error(f"Processor {processor.PROCESSOR_NAME} failed: {str(e)}")
                    results.append({
                        "processor_name": processor.PROCESSOR_NAME,
                        "execution_id": None,
                        "status": "failed",
                        "factors": None,
                        "error": str(e),
                        "execution_time": 0
                    })

        return results

    def _execute_single_processor(
        self,
        processor: BaseProcessor,
        inputs: List[ProcessorInput]
    ) -> ProcessingResult:
        """Execute a single processor (used by ProcessPoolExecutor)."""
        return processor.execute(inputs)

    def _emit_completion_event(
        self,
        underwriting_id: str,
        account_id: str,
        results: List[Dict[str, Any]]
    ) -> None:
        """Emit underwriting.processing.completed event."""

        event_data = {
            "account_id": account_id,
            "underwriting_id": underwriting_id,
            "executions": results
        }

        # Publish to Pub/Sub
        message_data = json.dumps(event_data).encode('utf-8')

        try:
            future = self.pubsub_publisher.publish(
                self.completion_topic,
                message_data
            )
            future.result()  # Wait for publish to complete
            self.logger.info(f"Emitted completion event for underwriting {underwriting_id}")
        except Exception as e:
            self.logger.error(f"Failed to emit completion event: {str(e)}")


def setup_pubsub_subscriptions(
    project_id: str,
    processor_registry,
    document_service,
    underwriting_created_subscription: str,
    documents_updated_subscription: str
) -> None:
    """Setup Pub/Sub subscriptions for processor orchestrator."""

    # Initialize Pub/Sub clients
    subscriber = pubsub_v1.SubscriberClient()
    publisher = pubsub_v1.PublisherClient()

    # Initialize orchestrator
    orchestrator = ProcessorOrchestrator(
        processor_registry=processor_registry,
        document_service=document_service,
        pubsub_publisher=publisher,
        project_id=project_id
    )

    def handle_underwriting_created(message):
        try:
            message_data = json.loads(message.data.decode('utf-8'))
            orchestrator.handle_underwriting_created(message_data)
            message.ack()
        except Exception as e:
            logging.error(f"Error processing underwriting.created: {e}")
            message.nack()

    def handle_documents_updated(message):
        try:
            message_data = json.loads(message.data.decode('utf-8'))
            orchestrator.handle_documents_updated(message_data)
            message.ack()
        except Exception as e:
            logging.error(f"Error processing underwriting.documents.updated: {e}")
            message.nack()

    # Start listening to both subscriptions
    subscriber.pull(underwriting_created_subscription, callback=handle_underwriting_created)
    subscriber.pull(documents_updated_subscription, callback=handle_documents_updated)

    logging.info("Processor orchestrator subscriptions started")


if __name__ == "__main__":
    # Example usage
    import os

    project_id = os.getenv("GCP_PROJECT_ID")
    underwriting_created_sub = os.getenv("UNDERWRITING_CREATED_SUBSCRIPTION")
    documents_updated_sub = os.getenv("DOCUMENTS_UPDATED_SUBSCRIPTION")

    # These would be injected dependencies in a real application
    processor_registry = None  # Inject your processor registry
    document_service = None    # Inject your document service

    setup_pubsub_subscriptions(
        project_id=project_id,
        processor_registry=processor_registry,
        document_service=document_service,
        underwriting_created_subscription=underwriting_created_sub,
        documents_updated_subscription=documents_updated_sub
    )
