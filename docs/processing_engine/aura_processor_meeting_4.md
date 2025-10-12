AURA Processor - October 09
VIEW RECORDING - 122 mins (No highlights):

---

0:00 - Chun Shao (Simple Code AI)
  So Jude, can you share your screen and quickly go over it? I can explain a little bit. Yeah, OK.  So if you go to the first one. All right. This is the overall. Now, I just talked with Adrees about this PubSub message.  OK. And we want you now to listen to the PubSub message sent out from database module. OK. All right.  It's the same format. It's just a different source you will listen to. through. Okay, like it's still underwriting created or underwriting updated, still the same information there, but like the document list could be a little bit different, let's add, it will include not only the file ID, it will also include like the stipulation type of it.  Okay, yeah, so this, this is like a, you will check, you can, you can from this message itself, you don't need to access the database, you will know whether, what kind of processes we need to call or not.  Okay, and probably you should have enough information, information, and Adrees, can we like include a URL that he can access where this file is at, where this file is stored at the data lake, so.  Like each that created it will include a document revision ID and the second one will be the URL of this file that they can access and the third one will be the stipulation type.  If there's no stipulation type it's going to be now and if it's now you don't you don't need to care about it.  All right. This is this is yeah. Oh, sorry. The stipulation type is already there. Yes, sir. OK. All right.  Yeah, fine. Like, yeah, we can we can check this. OK, so you need a revision ID and URI to access it.  OK, I really think that's just good. You can do it that way? Yeah. What if there's documents without any stipulation type?  How are you going to put it?

3:16 - Adrees Muhammad
  I think we should have a separate property with a stipulation type, not the name of the key.

3:26 - Chun Shao (Simple Code AI)
  We need to have what? A separate... Ah, okay. All right. So we put the stipulation type there, not the name of the key.  Okay. All right. Yeah. Yeah, in this case. So at least you need to do the aggregation. Okay. Not the aggregation.  Like you need to find out, okay, for this stipulation type, what are the documents? It could be easy. Like you can easily get everything.  All right. Okay, yeah. Yeah.

4:04 - Adrees Muhammad
  Okay. Yeah, sorry. I just, so yeah, we can add a property here. Yeah. That would be good.

4:12 - Chun Shao (Simple Code AI)
  Okay. Yeah. You can fix it later. Let me just quickly go through the whole flow chat. Go, go, can you go up?  Yeah. Yes. So you receive the message and you parse the message you received and try to find out the payload, the underwriting ID, okay, application form, and you will do three process.  One is filtration, the second is execution, the third one is consolidation. Okay. Now let's go to filtration. So for the filtration, first is you get enabled and auto-purchase the processes, okay, and, uh,  Then for each processor, you need to do this check. If you look at the left, okay, left, lower left, get execution list of this processor.  Okay, so this is a sub-workflow I will explain later. And if the execution list is now, which means that this process should not be called or generated, so it will not do anything.  Okay, just go back. And if it's not now, you need to add it to process ID and you need to add it to execution list.  And keep in mind that this execution list could be an empty array, it's different from now. So empty array, you still need to add this to process a list, but the execution list was...  Not be at anything because it's empty array, but it's different from now. That means even though you don't do any execution, but you still need to do the consolidation.  All right, this is pretty much straightforward. Okay, and the next is the Get Execution List. So Get Execution List is first you flat the message and match with any trigger.  Okay, if no match, then return now. Okay, this is why we don't need to do any like a processor consolidation because it doesn't match.  But if it matches, you need to generate a payload hash list. Okay, usually it's only like one for most of the processor.  It's just the one payload hash, but for bank statement, it's a list according to how many documents. Okay, and for each payload payload hash.  First you check whether there's any execution has the same hash. If yes, you replace the current execution hash. Okay, like in each process you have a field called a current execution, you just replace that hash.  Okay, if no, okay, you need to create a new execution and add it to the execution list and replace the current execution.  Don't forget it. The replace current execution has to be changed no matter whether there is a hash there or not.  Okay, you're going to replace it with the new hash and then return the execution list. Okay, so this is for like if they roll back to the previous document or they change the value back to  A value that is being processed before, we don't need to re-execute it, but we replace it with the current execution to make it match with the application form data or the document that is currently active.  Okay, so this is this one. And how to generate a payload hash list? I separate it. Okay, so to generate a hash list, firstly check whether this is document related.  So if it's purely application form, it's the value, like I check is the payload value now. If it's now, that means you delete it.  Okay, there is no value, so you need to remove the current execution. Okay, and return the empty array. That means you will not generate any new execution and you will remove the current execution.  So for this processor, the current execution is nothing, no current execution. Okay, even though there could be some execution listed, but they are all inactive.  Okay, because this is because you delete this value in the form that, for example, you delete the industry. Previously, they have industries chucking, then you delete it.  And since you delete it, there's no current execution. Okay, so we can understand. But if the value is not now, so we will use this payload value to generate the hash and return this hash as a list.  Even though this list only has like a one, probably, okay, has one value. All right. And this is the first.  The second is, if it's. Document related, okay. So it goes to the right and it has two situations. One is whether it's like for each document or for the totality.  So it's if it's for each for totality is similar to the to the payload. Okay, you need to check all the documents under the stipulation.  It doesn't matter how the change document they made. Okay, you need to check all the documents under this stipulation, even though there's only one document changed.  If it has like a six documents there, you need to generate the hash code of all six. Okay, for this part, can you understand?  I give you an example of JARUS license.

10:56 - Jude Pineda
  Yes, exempt, exempt, deleted documents, excluded. Yeah.

11:02 - Chun Shao (Simple Code AI)
  So every document like a JavaScript license, if you upload the two new documents and there is already four there, so now makes it total six.  And the payload hash should be based on the revision ID of all six documents. Okay. It's not only based on the two new documents.  All right. This is for all the documents. And if it's for each document, so it goes to the left.  Okay. For each document. So it will handle each one. And so it will check is this document deleted. If it's deleted, it will do the similar thing.  It will remove the current execution for this document. Okay. And so for this processor, it maintains a list of the current execution and you need to locate at the current execution for this document and remove it.  All right. And if no, if it's like not deleted, then you will generate the payload hash with this document version like revision ID and then check the next document and finally return the payload hash list.  Okay. So I think, is this clear? Like everything?

12:30 - Jude Pineda
  How about this question? Yes. I just have a question here. Are we going to only check the values? Because here it says, is payload value null?  But what if we have here, for example, this one here is null. But the others have value? Mm-hmm.

12:56 - Chun Shao (Simple Code AI)
  Yeah, it's just the base, based on this processor, which Which field or what's the field it looks at, for example, if it looks at three different values.  Yeah, yeah.

13:14 - Jude Pineda
  And one of it is null but the two have values.

13:19 - Chun Shao (Simple Code AI)
  Yeah, I think it should be all null. That means you are not able to run the execution. Oh, okay.  Okay, for example, like for the clear report, it could be done by like a business name. Is this possible for clear report if we don't have EIN number?

13:47 - Jude Pineda
  Yes, Chun, as long as the other fields are given. Mm-hmm.

13:53 - Chun Shao (Simple Code AI)
  Okay. So like it could only have EIN and don't have NAM. It could have NAM and don't have EIN.  And, but as long as you still can do, can run the execution, you run it, okay. But the payload hash, you need to determine, okay, the purpose is you generate the same hash, so you need to determine if the value is now, whether to include in the payload as a value now or excluded from the payload of now value.  And, uh, you need to make it consistent because it will change the hash. Yeah, yeah, yeah.

14:38 - Jude Pineda
  Yeah, okay, sure. Okay.

14:44 - Chun Shao (Simple Code AI)
  So, next will be very simple. So the execution will be parallel, run, and, uh, wait for all the execution completed, then you do the consolidation.  And for the consolidation, it's, like, sequential based on the... Like the index of the processor, okay, round the consolidation one by one, okay, and yeah, so here, I said at last you need to emit completion event.  I don't know whether you need it, the purpose is you need to allow the Zahiyu's module know that you updated those factors, right?

15:39 - Jude Pineda
  Oh, okay, so I will have to, I will have to group those factors by the processors, or do I have to?  Just give out all processors, but the thing is, if we're going to give out all the factors itself, there's going to be maybe overlapping factors with different processors.

16:03 - Chun Shao (Simple Code AI)
  Yeah, I don't think it will make a lot of change. It's just Sahil will do like how many different evaluations.  Okay, so like if you change, like if you have five processors, five executions here, or five processors need to generate to generate the factors.  Okay, one is Sahil received five messages emitted by the database module, and he need to run the evaluation five times, or he can like you but you need to like wait all the factors generated and update the database once.  So With all these factors, but in this case, if you have like a conflict of factors, like one factor from both processor, it will not be recorded for a factor that is in Z, that is consolidated from the previous processor.  Yeah, I guess you just do five times, five different updates, and I will talk with, I will talk with Sahil and see if it's necessary to keep all the records of evaluation.  I think we don't need it, it just keeps the most updated evaluation result, that's it. Okay, sure, sure. Yeah, so here you don't need to emit a completion event, you just do the consolidation of each processor, and you get it.  Factors, you update the database, that's it. Okay, and the database module well emit the proxy message to Sahil and told him, hey, these factors have been updated and you need to take care of it.  Okay, and even though, like, yeah, so this can be controlled by the database module, like even there are two processors, two execution, or no, two processors consolidation update the same factor, but the values are the same.  So the second update will not emit any Pubsa message because they didn't change any value. So that could save Sahil, like, but anyway, he already have factors like a hash code snapshot there.  It should be fine. Yeah, but it can save, still can save, like, don't need to run. On the hasher again, yeah, okay?

19:06 - Jude Pineda
  Yes.

19:07 - Chun Shao (Simple Code AI)
  Yeah, so I think the only thing left here, because you don't need to emit any completion message, so for the underwriting create and update, it should be there, right?  Next is the execute of the processor, like a force execution. Yeah. So for the force execution, if it's bank statement, it will include the document, but for others, it will not include anything.  Any document ID. So yesterday, I talked with Adrees. We found out that, OK, should we pass the execution ID to you?  What execution ID, Chun?

20:23 - Jude Pineda
  And if we go here, aren't we going to check if such execution exists or, ah, yeah, we're going to create new one, right?  But what do you mean by passing ID?

20:38 - Chun Shao (Simple Code AI)
  So if, OK, if they only give you a processor ID, OK, so what you would do is you will find out what's the current execution.  OK, if there's no current execution, it's simple, you just create a new execution and run it, right? If there is a...  Current execution for this processor. So what you need to do is you need to create a new current execution and link the current one to this one and replace the current with the new created execution.  All right. Yeah. I have a question.

21:41 - Adrees Muhammad
  Like, as you said, if I provide the execution ID, then it will be simpler. It will become simpler for him.  Like, let's say if we only provide the processor ID, it needs to go to the database and check whether we have a current execution or not.  more definitive. Has, if do not have, then we need to create a new one, there are different scenarios. But if I send the execution ID, if it's null, it means we don't have any execution against that, maybe.  And if is there any execution ID, you just go to that execution and perform. So isn't it simpler?

22:23 - Chun Shao (Simple Code AI)
  Which is simpler?

22:25 - Adrees Muhammad
  This one, if I provide the execution ID. You provide the execution ID.

22:33 - Chun Shao (Simple Code AI)
  That will be, yeah, I think that will be simpler.

22:38 - Jude Pineda
  Actually, by link, do you mean to supersede to the previous one? By updating the updated in the factor or?  Yeah, I get confused. Sorry. So, what I think, Chun, I'm sorry, I still didn't get that.

23:12 - Chun Shao (Simple Code AI)
  Okay. This is a processor execution. You have ID, okay? This is a fusion ID. You have organization, and which underwriting, and which underwriting processor, which purchase processor, and and the document lists, document lists, document lists, hash.  I think you already have, like, a payload hash. Do we still need, like, a document list, a hash? Okay.  And do you have?

23:56 - Jude Pineda
  Document list is just for IDs of the document revisions, right? Okay.

24:03 - Chun Shao (Simple Code AI)
  You have processor. All right. You have a status. You don't have a. Okay. This is for execution. For each individual execution.  Okay. Started at, completed at, created by, created at, updated at, updated by, updated execution ID. Okay. This is what you mean by link.  Yeah. This is what I mean by link. Yeah. Okay. Got it. Yeah. Let me think about the UI. So in the UI, for each underwriting, and for the processors, we have a list of all the processors.  And for each processor, we have a column called Executions. So it will list all the executions of this processor, along with their status of this execution.  Is it pending, or running, or completed, or failed, or canceled? Okay. And if it's a bank statement, so it could be multiple processors listed there.  And we'll have a couple of them marked as active, like at the current execution. Okay. And what we can do is either we can right-click on any execution and choose rerun it.  Okay. That means it will... Rerun this execution with the same hash code, with the same payload. Same hash code means same payload.  Rerun it and get the result and update the link that is the one that you showed me, updated execution ID.  Okay. And so it will replace. Okay. They will not replace. Yeah. Adrees, can you see that? What do you want to say?  Yeah.

26:33 - Adrees Muhammad
  Like in case of, in that case, you said updated execution ID will be changing. Like if we create a new execution, then it will be changed.  If we just roll back, then it will not. In that scenario, we will create a new execution, right? Yes, we'll create a new execution.

27:00 - Chun Shao (Simple Code AI)
  Then it will be upgraded, yeah. So this is based on the payload of this execution. And if this execution itself is not active right now, it will not replace the current execution of this processor.  If this execution is current execution, it will replace it. OK. It will replace it with the current execution. All right.  This is one thing. They provide an execution ID. That is, they specify, OK, I want to rerun this execution.  Another way is we rerun the whole processor. They don't provide any execution ID. They just provide a process ID.  We rerun the whole processor. It's key. Thank you. So it could be three different things. One is this processor don't have any execution.  It could be it's not automatic running. Okay, so they started manually. So in this case, this processor will go to find, okay, what's the payload and generate execution based on the payload and run it.  And it could be no execution be generated because there is no payload. For example, there's no document in the driver's license and this processor cannot run it because no payload.  Okay, this is the first situation. The second is it has execution. All right. And this execution is, but there is no active execution.  So it will based on its payload. All And if, similarly, if it has payload, okay, if there's no active payload, will give error.  So if it's payload, it will generate payload and create execution and try to find out if there is any hash existing current execution and replace it, okay?  Okay, and this time, no matter this execution, the current execution is active or not, it won't mark this execution as active, okay?  Because this is a processor layer, reach a rerun, okay? It's not based on one execution, it's the whole processor, so it will replace it.  The third situation is if this processor is bank statement, so that means it has multiple execution being activated, being active.  Should we, like, yes, we should run for each document, because this is like, we didn't specify any execution, so we should re-run the bank statement, and for each document, it will generate the hash code, and based on the hash code, it will generate a new execution, and this execution will replace the same hash code execution, and if that document don't have any current, it will mark it as current.  If it has, it will replace it. Yeah. So for this request, I guess we need these two things. Okay.  The first ID should not be the underwriting ID, and the processor should be underwriting process ID. ... ... ...  Yeah. Okay, and we don't need this processor, Adrees, yeah. Can I add something here?

31:16 - Adrees Muhammad
  Like, in the current, based on our current logic, what we will do to make the execution as current is to go to underwriting processes table and the changes current executions list property.  Okay, that's what we are doing right now. Let's say, in case of a driving license, we will have one execution, so the array will have one, maybe property, one, and one, sorry, execution ID.  And in case of bank statement, we will have three, so the array will have three execution IDs. So, in case of, let's say, a user tried to rerun a processor, processor execution, rerun the processor execution, and  And it may be, in the case of bank statement, it will be one of the current, maybe you can say, if it's a current execution, one of the current executions of the bank statement, because bank statement will have multiple executions.  So we will not, and we will create a new execution in that case. We will not replace the current execution list in that case.  We will just append that ID to that list.

32:31 - Chun Shao (Simple Code AI)
  But then you can remove the previous ID. Yeah, you need to remove the previous ID if we know that there is any, like, executions related to the same document exists in the current execution list.  Yes. Yeah, correct. Okay, so we need the underwriting process ID. We don't need the processor. Okay, we don't need this one.  Yes. And they could specify execution ID or like, do we need the document list? I don't think we need document list because this is just the execution related or process related.  It's not document related.

33:31 - Jude Pineda
  As you said, the processor itself is executed because it's not auto.

33:38 - Chun Shao (Simple Code AI)
  Can you see that again?

33:41 - Jude Pineda
  Let's say the processor itself is not automatically executed. So it has to be manually executed. Yeah. So how am I supposed to know what documents should I process if there's no document list?  That's something that you to Right. Hello. That's so much Hello.

34:01 - Chun Shao (Simple Code AI)
  Hello. Okay, so like a, we can like a rerun the whole processor, it will run for each document, right?

34:13 - Jude Pineda
  Yes, Jim, but what if there's no execution? Because it's not automatically executed.

34:20 - Chun Shao (Simple Code AI)
  Yes, then you will run it from the beginning. Like if it's under the processor tab, list of the processor, and you want to rerun from that part, you only, the only two things you need to be there is underwriting process ID and execution ID.  Okay, if you provide underwriting process ID, will run the whole, like a processor. So, so this is our execution, not really a manual execution.

35:01 - Jude Pineda
  Because if that's the case, we're only trying to re-execute up previous existing execution. Am I correct? Yeah, it's like you can say it's called re-exclusion.

35:14 - Chun Shao (Simple Code AI)
  It could be like the first time execution. Okay, it will be the same. But keep it there. Keep it there.  Sorry, I need to tell you, okay, another thing. So if it's under the process tab of one underwriting, the underwriting process ID and execution ID should handle all the possibility that could operate by the user.  But another one is like if it's in the document list. So if it's in the document list, should we like a list to the execution?  Besides the document. I'm sorry, Chu. Okay. So in the tab of document list, should we list the execution that is related to this document?

36:24 - Jude Pineda
  Is it necessary?

36:29 - Chun Shao (Simple Code AI)
  It could be necessary. For the bank statements, if we want to view the execution of these documents, and for example, the bank statement, want to know the result of it.  Then we probably will be convenient for us to put the executions that related to this document and listed there.  So, do you think it's necessary? necessary? So, Bye& you See

37:03 - Jude Pineda
  Oh, we could add that too.

37:05 - Chun Shao (Simple Code AI)
  Jeremy, do you think it's necessary when we list the document, we put the execution that is associated with the document besides it, so the user can check the result of the execution of this document, the processing of this document?

37:27 - Zhanfan Yu
  Yeah, I think it's...

37:29 - Chun Shao (Simple Code AI)
  Okay, if that's the case, then we need to, we need probably need to put a document ID here. Sure.

37:45 - Adrees Muhammad
  Fund, like, one execution can have multiple documents. So, we need to enter the scenario as well. if we take consider in this scenario, then we should add...  That, I don't think so, because that execution result is not based on that one document. It's based on the, let's say, four documents, in case of driving license.

38:14 - Chun Shao (Simple Code AI)
  Yeah.

38:15 - Adrees Muhammad
  So we are just adding that this execution result based on this document, but it's not correct. It's based on four different documents.

38:24 - Chun Shao (Simple Code AI)
  Yeah. Okay. So we shouldn't maybe add two ways. Okay, one, okay, there are two ways to solve this. One is, like, we put the same execution after all these documents.  So each document will have a execution listed behind, like, a sited, but they are the same, the execution. This is one way.  The second way is, it's like a stipulation based. So we list the execution besides the stipulation instead of the document.  Okay. Okay. But, like, uh... ... Is it, okay, which way is better, how to design it, for the document, probably, okay, if we want to make it simple, okay, we will not, okay, all right, should we allow the user, okay, let me ask you this question, should we allow the user to run the processor for one document, like a bank statement, should we allow the user to do that?

39:58 - Jude Pineda
  Yes, you know, I don't think that's a problem. Mm-hmm.

40:04 - Chun Shao (Simple Code AI)
  Okay. Adrees, do you think it's good? In case of bank statement, we can.

40:12 - Adrees Muhammad
  But if execution needs multiple documents, so it will fail. Yeah.

40:21 - Chun Shao (Simple Code AI)
  For multiple documents, we just don't put documents ID there. It's just like the process ID and it will run the whole stipulation documents.  Yeah. But if like we want to run the bank statement processor with a particular bank statement, so we can include the third item in this payload, which is document ID.  Right. Yeah. And I think we need, I just need an ID. That is enough. Do we need to include a list?  Or it's just the one document. Is it enough? So in the future, which way it is? Probably a list could be more expandable in the future in case there is some like a weird situation for a processor that we can specify which files you should include in this execution.  Yeah, probably list. List is better. Document list. Yeah.

41:55 - Adrees Muhammad
  Chun, if we have the stipulation type in that payload, we can easily find out what What other other documents we need to execute that?  Yeah, yeah, we don't need like a, yeah, we don't need a stupidity type.

42:10 - Chun Shao (Simple Code AI)
  We just have the underwriting process ID. We know everything. Yeah, yeah, yeah, correct. So we can find other documents.  Yeah, yeah, yeah, we can, yeah, we can keep these documents list. Okay, in case, it's not happening now, in case, let's say, for example, Java's license, I uploaded six files, and by default, we will run the analyze on all six images.  Okay, and let's say there is a user. Okay, he has a change request. I only want to choose this four to be run by this processor, and I don't care about the other two.  And we told him, oh, you can delete those two images, and it will automatically rerun the driver's license processor, and he said, I'm not glad to do  That I want a function that I can choose this for documents for the processor to run it. Then we can use this function to do that.
  ACTION ITEM: Update workflow chart for manual processor execution. Include logic for handling execution ID, document restoration, and consolidation without creating loops.
 - WATCH: https://fathom.video/calls/435532261?timestamp=2599.9999  Okay, so keep documents list. That's good. Yeah. So keep it as a list. All right. Yeah. Good. And yep, that's that's it.  So you need to, okay, update the left workflow and workflow two. No, This one. Yeah. On the left side, just start everything.  You remember what I just talked about, like handle different situation?

43:53 - Jude Pineda
  I just said, you're going to have to listen to the execution idea and just, uh, Okay. Okay. Okay. Okay.  Okay. Execute. And then we're going to link it to the existing and then replace it by updating the updated execution ID.  Okay.

44:13 - Chun Shao (Simple Code AI)
  So first, what do you need to check is if there is an execution ID. Okay. If it's execution ID, what you will need to do is you get these executions, hash code, okay, payload, everything, and then create another one and then replace it.  Okay. And, uh, and, uh, create a execution. Okay. And run it. This is a with execution ID. If it's without execution ID, then it's, uh, it's, you need to check whether it has a document list.  Okay. If it's not have document list, then you'd like to rerun the whole process and everything and create the hash code.  They're like, get the hash code list, everything, okay, based on the current, like a payload, everything, you, you probably can reuse some workflows we defined up there.  Okay. And if it includes the document list, probably, you need to like a check whether this is like a for each document or for all documents.  And you basically, if it's for all documents, okay, what you would do is, okay, based on the document list, you generate a payload, hash, everything, and create it.  If it's for each document, probably same thing, for each document, you do generate a new execution, everything. So, yeah, I'll rewrite the flowchart on the left, okay?  Okay, sure. Yeah, yeah. And I will check it. Once you finish it, I will check it. All right. Okay.  This is the second workflow that is manually execute a processor. Okay. All right. Yeah. And next, workflow three is processor update.  Okay. What does this mean, update? Yeah.

46:32 - Jude Pineda
  This one is supposed to be consolidated only. I can't remember the channel if you don't know if you think this is deemed unnecessary.

46:47 - Chun Shao (Simple Code AI)
  It's just a rerun the consolidation. Okay. Okay. Okay. Okay. A execution? Oh, yes. So let me see what's the payload you put in underwriting ID and execution ID.

48:19 - Jude Pineda
  Chun, I think this one now is just the same as workflow 2 because I think workflow 2 is actually for manually executing.  I like a processor with the previous execution.

48:37 - Chun Shao (Simple Code AI)
  No, this is not like create any new execution. just to update the current. Ah, Sorry, I forgot.

48:48 - Jude Pineda
  So roll back.

48:50 - Chun Shao (Simple Code AI)
  What do you mean roll back?

48:52 - Jude Pineda
  We roll back to that specific execution, Chun. Let's say from your given scenario, what if the... ...the... ...with... ...that...  ... It's a new execution of this triggered processor because we have, let's say, like deleted EIN. We can use the previous execution to do a rollback, maybe update its original application form data.  Okay. All right.

49:24 - Chun Shao (Simple Code AI)
  Can we change our mind? Let's maybe, like, do it this way. Okay, like, Okay. It's fine. All right. It's fine.  Fine. Yeah. I was thinking, like, you only change the data, roll back everything, and then the database module will emit a message.  Oh, we have updated, and you catch it updated, and you will find out. It's fine. fine. fine. Same HashCode execution and the market has, no, this is like a, it's not good way to do that.  So you still need to, okay, rollback, execution rollback. I believe this is like the updates, the current execution of this processor.  Okay. sir. Yeah. And then message received, well, what is this one? Execution rollback. The second, the, after start, the first is rollback, the second is a message received, what is message received, the execution rollback?

50:41 - Jude Pineda
  I mean, I'm sorry, this one is just a pedo-junk, sorry about that. okay, the first two is just a message received.  Maybe we, it should be a, first message received, sorry. Ah, okay, okay.

50:58 - Chun Shao (Simple Code AI)
  Okay, uh, what's your, we're very. Very simple, like you don't even need the underwriting ID. Just execution ID is enough.  Yeah. And then you find the execution. Okay, execution exists. And success.

51:18 - Jude Pineda
  Oh, yes, Chun, do you think we should allow our rollboxer to fail the executions? Okay.

51:26 - Chun Shao (Simple Code AI)
  If it's not exist, what do we will do? I will just fail it. Yeah. Yeah, okay. What if, and what do you mean success?

51:38 - Jude Pineda
  If that execution is failed, let's say, for example, do we allow them to like roll back to the specific execution?

51:48 - Chun Shao (Simple Code AI)
  Ah, okay. To, okay. You mean this execution is failed and it should not be able to mark it as active?

51:58 - Jude Pineda
  Yes. Okay, good. Okay.

52:01 - Chun Shao (Simple Code AI)
  So, We will go to no, fail, and what's the next, goes to, go all the way down. I want to see where it goes.  Okay, end. All right, so if it exists and succeeds, processor type. Is it application-based or documented? think we can restore application form from execution payload.  Okay. And reactivate execution. Mark as current. Disable current execution. It's different.

52:38 - Jude Pineda
  Yeah, this needs to be removed, I think, we're just going to update the execution system, that specific purchase processor.  I mean, the underwriting processor.

52:54 - Chun Shao (Simple Code AI)
  Okay. All right. First, if it's document-based, you will not do anything? All right. Thank

53:01 - Jude Pineda
  Yeah, don't think I have to do anything, because those revisions are handled by data collection, just except for this application from data.

53:12 - Chun Shao (Simple Code AI)
  Why not, like I said, those revisions as the current revision for the documents?

53:23 - Jude Pineda
  Oh, yeah.

53:25 - Chun Shao (Simple Code AI)
  Yeah, I completely missed that question.

53:28 - Jude Pineda
  I think so. Yeah, and what if there is deleted?

53:40 - Chun Shao (Simple Code AI)
  What if they are deleted?

53:46 - Jude Pineda
  So you mean that if the revision, a document revision used was deleted? Okay, yeah, let's say that.

53:54 - Chun Shao (Simple Code AI)
  Okay, you have like a bank statement processor. Okay, you uploaded it. And then you delete this document, and the execution is disabled because you delete the document, right?  So there's no current execution. And then you right click on this execution and activate it again. All right, what are you going to do with the document?  I think we should just fail each other.

54:27 - Jude Pineda
  Yeah, I didn't see that use case.

54:30 - Chun Shao (Simple Code AI)
  Yeah, so in that case, because this document contains the revision ID as the payload, in the payload of that document, then you should go to check that document.  First, is it deleted? If it's deleted, then you mark it as undeleted. Second, is the revision ID same with the current revision ID?  If not, replace it with the current, you should be And for the reason I do. Right? This is what we should handle with the document.  Okay. What about the other documents? Should we mark them as deleted? That's it. Okay. This one. You have a JavaScript license and have four documents uploaded and it will do execution.  And then you added another two documents. So it comes to total six pictures in the JavaScript license and they do another execution.  So the first execution has four images. The second execution has six images. And the second is the most current one.  Then you right click on the of the first execution. And the Check it as active, all right? And you will go to the system and find out using revision ID to check the four.  They are all most current active documents. OK, but I forgot that you have another two listed there. It's not deleted.  And they are not in the payload. Their revision is not in the payload. So you need to delete those two documents.  That is not in the payload. Oh, OK. So for document space, you need to do three steps. The first is, you have the payload, OK?  So the first, you re-enable any document which is deleted and that is in the payload. Second, you delete all the documents which is not in the payload.  And the third, you check the remaining documents, whether their revision ID is the most current one. Okay? This is what you need to do.  But, remember, this is only for, like, all the stipulations. If it's document-based, like a bank statement, you don't need to delete other documents.  Okay, you just, like, make this document revision ID, you update it. Or, like, if this document is deleted, first you recover this document, then you mark this, like, the revision ID.  So, you don't execute the deletion of other documents. This is only for bank statements. You don't do the deletion of other documents.  You, the first, You Okay. Yeah, it's going to be complicated. Okay, Adrees, what's your question?

58:16 - Adrees Muhammad
  Yeah, so let's say in case of bank statement, we have the first we have, let's say, a bank statement of only FAB.  And we run an execution. Okay. And then we add, let's say, two months more bank statements. And we just make one as disabled, FAB one.  Okay. We make that disabled or just make a mark as deleted, that FAB execution. Now we have only two executions.  Okay. We have the document of FAB one as well in the database. Okay. Now, let's say I, uh, uh, uh,  All back to that Fab execution. So I need to reactivate that particular document as well. Is that correct? Is it bank statement or not bank statement?

59:24 - Chun Shao (Simple Code AI)
  Is that processor? Yeah, it's a bank statement. No, you don't need to deactivate the existing two. No. No. Yeah.  Uh, Chun, I need to leave now.

59:40 - Zhanfan Yu
  I have another meeting with Spencer. Oh, okay. You guys can continue. Yeah, sorry to interrupt. Yeah.

59:46 - Chun Shao (Simple Code AI)
  Okay.

59:47 - Jude Pineda
  Uh, Chun, can we, uh, should we allow, uh, like, the activation of execution or, or, do we leave it at as, this?  Like let's. They don't want this output anymore for this specific processor. Can we disable this execution so that all of its factors won't be included in that?

1:00:24 - Chun Shao (Simple Code AI)
  Okay. Sorry, I'm replying a message. Can you see that again, Jude?

1:00:31 - Jude Pineda
  Yes, Chun, let's say the underwriter don't want to include the specific processor's output. Do we allow them to disable execution?

1:00:44 - Chun Shao (Simple Code AI)
  Let's say this one is the current. Okay. Yeah. Yeah. Disable execution. Yeah, probably. Yeah, we should allow them to do that.  Okay, okay.

1:00:57 - Jude Pineda
  I see that again. Then what are we going to do?

1:01:00 - Chun Shao (Simple Code AI)
  Okay. will here. Okay, okay. You We remove all those factors, Jude. We'll do nothing, right? With the application form and the documents, will not do anything.

1:01:15 - Jude Pineda
  For the form data and documentation, I think, yeah, we do nothing but just the factors, I think.

1:01:22 - Chun Shao (Simple Code AI)
  Yeah, just remove it. If it's like the current one, we remove it from the current. Oh, yes, sure. Yeah, and that's it.

1:01:32 - Jude Pineda
  We have to empty the executions list.

1:01:39 - Chun Shao (Simple Code AI)
  Not, yeah, I don't know what you mentioned, the execution list.

1:01:47 - Jude Pineda
  Remove it from the execution list.

1:01:49 - Chun Shao (Simple Code AI)
  Yeah, not empty, because it might have others there. You just deactivate one. Oh, yes, sure.

1:01:58 - Jude Pineda
  Yeah. Yeah. yeah. Okay. So are you...

1:02:01 - Chun Shao (Simple Code AI)
  Clear now about this activation. This could be a little bit complicated. So my suggestion is any application form payload, even if it is now, you should include in the payload as it's now.  Otherwise, you will not be able to go back to the correct endeavor. OK. OK.

1:02:32 - Jude Pineda
  Yeah.

1:02:33 - Chun Shao (Simple Code AI)
  Keep the current data, even if it's undefined, you cannot find it. But when you compose the payload, put it as now.  OK. And then we can go back. Otherwise, like you're missing it, and you will miss the update, the payload to the application form.  OK. Now, I have a a second question. OK. OK. Thank you. Let's scroll down the flowchart a little bit.  Yeah, this one. So you will see you need to restore the application form from execution payload, right? You restore it.  Yes. Yes. And after you restore it, you mark this as current execution. Okay. Let me tell you. So once you restore it, actually, you will call the database module to update the application form, right?  Yes. And the application of the database module will emit a Pubsom message for this update. Okay.

1:03:49 - Jude Pineda
  Can we add like a flag to say that this, let's say a flag to the message that this specific update is from the processor module so that it won't have to trigger.  Are these specific processors again? No, no need.

1:04:06 - Chun Shao (Simple Code AI)
  My suggestion is this. Okay.

1:04:10 - Jude Pineda
  You first reactivate the execution.

1:04:13 - Chun Shao (Simple Code AI)
  Mark it as current. Okay. Then you do this restore data thing. Okay. All right. Okay. Yeah. And, yes, then, the database will emit an update message, and you will receive it.  And once you receive it, you will calculate the payload, and you will generate the cache as usual as the previous one.  And then you will find out that, okay, this execution is already there, right? Yes, Gene. Yeah. So, the execution is already there.  If you go... Let's check what we will do in the previous workflow, go all the way up, yeah, yeah, they have the same hash, right?  Yes, sir. So you just replace the current execution, right? Oh, yeah, it will replace it, but because it's the same, you're already there, so it doesn't matter, you replace it or not, and then it will do the consolidation after this, so you don't need to do the consolidation in your workflow 4, because this consolidation can be taken care of by the restore application form.  Yes, that makes sense, yeah, it could end here. Yeah, and even if that's even possible that you don't update it here, you handle it by changing this application form data or the document, versions, and it will handle it automatically.  So you don't need to do anything here. Is that possible? Or is that good? Oh, yeah. Anyway, because you change the document and it will emit a message, or you change the form, it will emit a message, and you will handle this message by mark which execution is most current and call the consolidation functions.  But actually, the front end, the APCI need to handle this. Okay, the API needs to handle that to give a message back quickly.  Okay, so this is the case the UI will right click on One Next Fusion and choose, say, okay, I want to mark this as, I want to activate this.  So it sent a message to the back end of the API, the API handle this and probably will update in the database.  Okay, this current execution has been updated. Okay, and send the response back to the front end immediately. Okay, That was pumpkin parenthetically.  Okay. do you do with the writes? Okay. Yeah. Correct. Adrees, what do you think about this? Because the front end should get the message immediately.  It shouldn't wait till all the consolidation and everything is done and then it returns, okay, this has been done.  So it's better that we update the message there, then we return the result and allow the rest of like we change the document, we update the application data in the backend, but we return the success of replace the the execution immediately to the front end so they can update the UI to let the user know, okay, this has been updated successfully.

1:09:03 - Adrees Muhammad
  Yeah, but the message should be meaningful so that you can let the user know what's happening.

1:09:13 - Chun Shao (Simple Code AI)
  How are we going to handle that? So the actual update the database to replace the current message as this one, should we should this operation be called in API or here?

1:09:59 - Jude Pineda
  Thank you. You

1:10:11 - Chun Shao (Simple Code AI)
  Okay, so we need to pay attention that we will not create a loop, okay, it will loop, and change here, change the document, document changed, and we change the ID, and we change the ID, we change the document, change the document, change the ID, so we, the, the basic is, like, we don't create a loop here, right, yeah, so, Yeah, so,  So we make this message a special one. Like, this is a special message that we update the, like, activate the execution.  So the database will have a special operation. It's different from other operations. It's a special function that we activate the execution, and it will update the database.  And then, API will return to the frontend, and the meantime, it will... We need a message to help you that we update, we activate this execution, and you will do everything, but without like a reactivate execution, like mark as current, this will be handled in the database module, and you will not do the consolidation, because this will be handled by by the operation, you restore the full application form or the documents, but this will not create a loop, because the message it emitted is underwriting update, and underwriting update, when they handle that, it will find out already there is this kind of execution, and it already has been in market.  As the current one, even you overwrite it, doesn't matter. And it will emit a message handled by the processor to do the consolidation, but without any execution.  Yeah, that's it. Okay. So here in this workflow, remove the reactivate execution, mark as current. No, the reactivate, remove the reactivate.  No, no, no, you'll remove the other thing. Remove the reactivate. No, no, no, no, no, no. Undo it. Undo it.  Yeah. You'll remove the disabled. Disabled. the Disabled current is also, yeah, so you move the whole thing, yeah, you just change it and that's it, yeah, to the end.  So basically you changed it and that's the end of it.

1:14:40 - Jude Pineda
  Well, I'll just update this later just so I'm a little confused.

1:14:46 - Chun Shao (Simple Code AI)
  Yeah, okay. Yes, so where should we, like, check whether this execution exists and the success? Yes, should we check it here because  It's already been changing in the database, so this will be checked by the database module.

1:15:15 - Gene Rellanos
  I have a question. If it's failed, don't allow them to restore to that point, right?

1:15:20 - Chun Shao (Simple Code AI)
  If it's failed, should we allow it?

1:15:28 - Gene Rellanos
  I think of no, because in the workflow, execution exists and success.

1:15:33 - Jude Pineda
  If no, just fail.

1:15:35 - Gene Rellanos
  So I think maybe we can just maybe disable the button in the front end, like if there's a button there, if we can restore to this point, if it's the status of that execution is failed, we can maybe just disable the button so that we don't have any execution to the database.  So should have any queries, save the data.

1:15:58 - Chun Shao (Simple Code AI)
  Well, theoretically, you. You should allow them to roll back to a field execution. No problem. OK. Yeah. Yeah, but we can prevent it in the front end.  But you should make sure this execution exists. This can be handled by the database module. So if they cannot, like you give an execution ID and database module said, oh, I cannot find this execution in the database.  Then they will return an arrow. That's it. And when they emit a message with an execution ID here, the execution should exist.  OK. And what you will do is just to base on the information, you will restore the application form and restore the documents.  OK, and the base of the... Processor, two steps of documents must be done. The one is restore the delete one.  The second is update the revision ID. And if it is not back statement, you should run the deletion of documents not in the list, in the payload.  OK, yeah. So, yes, so the first thing you get this message, first thing you need to find out is the payload.  And based on the payload, do this. That's it. Yeah. So, yeah, you can update this again. OK. And do you have, like, disable?  I got featured.

1:17:52 - Jude Pineda
  So I don't think you need to handle disable.

1:17:55 - Chun Shao (Simple Code AI)
  Disable is just API receive disable and call the database, the database disabled it. It could emit a, a. So you say, hey, I disabled this execution, but nobody will listen to it, right?  Yeah, actually, yeah, that makes sense.

1:18:11 - Jude Pineda
  Yeah.

1:18:13 - Adrees Muhammad
  Chun, which execution will be disabled? Because in the payload, we only have an execution ID, which will be activated.

1:18:23 - Chun Shao (Simple Code AI)
  In the payload, we only have execution ID, and then what?

1:18:27 - Adrees Muhammad
  Like in payload, we only have execution ID, which will be activated. Which is previously not activated, so it will be activated.  But which execution we will disable? We don't have any ID. Yeah, that is a separate API.

1:18:45 - Chun Shao (Simple Code AI)
  So this is like we need to go through the API. Okay, so it's seen the API is not here.  For processor module, it will not listen to any message that execution is disabled because he will not do anything.  He will not roll back the application form data. He will not roll back the documents. He will not create a new execution.
  ACTION ITEM: Implement processor module to handle activation/deactivation msgs. Include logic for restoring app form data, updating docs, and consolidation w/o creating loops.
 - WATCH: https://fathom.video/calls/435532261?timestamp=4759.9999  He will not say, hey, wait, he needs to do the consolidation. Right? Do you need to do the consolidation to wipe out all the factors?

1:19:30 - Jude Pineda
  I think so, Chun, if you need to wipe out all the factors.

1:19:35 - Chun Shao (Simple Code AI)
  Yeah. Right, Adrees? If he disabled a execution, he needs to do the consolidation.

1:19:54 - Adrees Muhammad
  So, should he need the execution ID, which will be We disabled, because I'm not confused here, like he only got the execution ID, which will be activated.  Let's say in case of driving, in case of a passport or driving license, we only have one execution which will be activated at that moment.  Okay, so we need to disable the other one. Okay, that's, that's one thing. In case of bank statement, we don't need to maybe disable the other one because we can have multiple executions.  If we want to disable, then we have that ID as well to disable that. So how he will handle that, how we will disable that, because he needs to call that machine to disable it.  So it's, it's separate.

1:20:43 - Chun Shao (Simple Code AI)
  It's separate. It's not listed here. The, the disabled execution will cause a result, could cause a result that no active, active execution exists there.  It's just like a, we, we disabled it. Already disabled it?

1:21:05 - Adrees Muhammad
  We just disabled it.
  ACTION ITEM: Create API endpoints for activation/deactivation of executions. Implement logic to update current execution list, handle bank statement case, and emit appropriate msgs.
 - WATCH: https://fathom.video/calls/435532261?timestamp=4865.9999

1:21:07 - Chun Shao (Simple Code AI)
  We didn't activate anyone. We just disabled one. We are not using another one to replace it. We just disabled this one.

1:21:16 - Adrees Muhammad
  Okay. You mean, let's say we got a request from the front end to activate the execution. In API module, we will call the database module to disable the execution.  Then we will call the, then it will further proceed with the processor and...

1:21:34 - Chun Shao (Simple Code AI)
  No, no, no. Activate is activate. Disable is disable. You will have two functions in database module. And you will have two API endpoints.  One is activate, one is disable. One So let's say for disable, for example, we have like a... ... ...  ... ... ... Java's license processor and we have execution with two documents uploaded. And what they will do is they disable the execution.  And then we will not do anything because it's just disabled and there's no current execution activated for this processor.  That's it. Okay, we will not, this is what we discussed before, we will not mark those two documents as deleted.  It's because we don't have any current execution there. Okay, so that's it. But we need to do the consolidation because the execution changed.  So what you will do is your API will listen to a Disable request, and call the database module to disable, to remove it from the database, from the current execution list of this processor, remove it, and then emit a message, say underwriting execution disable, and Jude will listen to that message, the only thing he will do is to consolidate this processor, that's it.  Okay. what about activate? So activate is, API will receive activate request with a execution ID, and you will call the database module, a special function called activate.  And this function will, first based on the execution ID, find out what process ID it is. And it goes to that process ID database table.  And, uh, uh, to replace okay to append this execution id into the array list okay and remove the previous one okay now there's a little bit complicated so if it is the processor the type is not the bank statement processor you know it will replace everything just like a we only have one active execution there but if it is bank statement what we will do is we need to find out the execution related document id and try to find out is there any existing execution id which also have this document id  Okay, if it has, then we remove it from the ArrayList, the current ArrayList. Okay, then emit a message, include this execution ID, say, okay, this execution has been activated.  All right, and Jude will receive this message and run this workflow. Basically, it's to roll back the application data, all the documents, and that's it.  And your database module, when he rolls back, I mean, it will call the database module to roll back. And then what he will do is emit a message, hey, this document has been deleted, and this document has been revised.  Okay, and it will, okay, hold on, we need to be careful, because we don't want to emit a couple messages.  There are some documents that will be removed, some documents will be updated, revision ID, some documents will be marked as undeleted.  Okay, so we will make sure all this message, all this change will be handled once. Otherwise, it's gonna create like each document if we update, like if we update it separately.  So we will have maybe five, six different hashcodes for different combinations of the document and it will draw a lot executions.
  ACTION ITEM: Implement database module funcs w/ emit msg indicator. Create 2 types: basic CRUD (no emit) & complex ops (w/ emit). Ensure transaction support for multi-op funcs.
 - WATCH: https://fathom.video/calls/435532261?timestamp=5215.9999  That's not good. So we will make sure the update will be all combined all together. Wow. Is that good?  Wait? Yeah. To design? Yeah.

1:27:06 - Adrees Muhammad
  So for that, what we can do, let's say, for the simple CRUD operations, get, update, upload, we will not emit any message, okay?  Let's say. For the, we will emit message in a function which maybe is doing multiple operations or which needs to emit a message.  Let's say in that case activate, we will have a function activate in the database module, which will have a transaction.  So it's performing multiple operations. So it's just maybe updating the document and doing other stuff. It will not emit any message, but as soon as the transaction will complete, it will emit a message.  So we can, we will have two types of functions in the database. First are simple query functions, which will not emit any message.  We just do the. Spread operations, just simpler things. The second functions, these are the functions which are performing the main tasks, let's say activate or and other, which are just using those basic functions to implement the business logic or you can say.  And they have transactions, those will emit the, I guess, these events. So is it, it will, I think it will work, what do you think?  Okay.

1:28:35 - Chun Shao (Simple Code AI)
  Okay. Ah, so is it, there's something like a transaction and so let me ask you, like in this case, if the activate of one execution includes like a delete one document, update one document, and how you're going to handle it.  How Thank How combine it and only add it to one message instead of two messages?

1:29:09 - Adrees Muhammad
  OK, so we have a function to delete a document, OK? A basic function which will delete the document. And a basic function which will maybe append the ID to the current execution list.  So we have a main, now we have a two basic function and one main function which is the activate function.  What I will do inside the activate function, first I will let's say delete the document. And in the next function I just maybe append the in the current list.  These two functions will be called inside a transaction, OK? When we commit and below we have a commit statement, when we commit the transaction, after that we will emit the message to underwriting.execution.activate.  That will be received by the Jude. And let's say if because of any reason the transaction got an error or if one thing fails, maybe appending in the current execution list will fail, then the execution transaction will fail.  Then we don't need to emit any message in that case. So it will be handled by the exception or other things.  So after the successful transaction, after the successful completion of these operations, then only we will emit the activate function.  So we have two categories of functions here. can say first are the base basic functions. We just perform the basic functionalities like utility functions, you can say, or the basic operation they will perform.  And second, we have a handlers of the routes and alerts of the routes or the repository function. you Like here, the activate, and we will have the other as well.  These functions will emit the events, not those functions will emit the events. Okay.

1:31:15 - Chun Shao (Simple Code AI)
  Does that make sense? Yeah, yeah. So can I clarify that? Yeah. To update, like the rollback of the documents, like on delete one document and update another document, these two operations will be handled in database module, or like it will be handled in Jude's module, but call the function you provided, which one will be the one?

1:31:47 - Adrees Muhammad
  Okay. So if Jude need to perform any business logic after one operation, database operation, then we cannot add all the operations in the transaction because Jude need to perform.  Any business logic or other type of stuff. But if you don't need to perform any business logic, then we can combine those in a transaction.

1:32:17 - Chun Shao (Simple Code AI)
  Well, say, if you don't need to perform any business logic. Yeah, then we will just call those in there.  Okay, Jude, what's your opinion on how we should handle this? Like, this could be like this rollback. Basic idea is this could cause the change of the documents.  Okay, and we don't want to create any like intermediate hash code status of the documents to add extra, you know, this processing.  Okay. Okay. Now,

1:33:06 - Jude Pineda
  Let me think about it, Chun.

1:33:12 - Chun Shao (Simple Code AI)
  Also, let's go, let's probably, let's go back. For example, now we have an underwriting and we're uploading documents. Okay.  And so what if they upload document one by one? The driver's license, they upload one document, wrong, processor, failed.  Upload another image, second image, they're wrong. Okay, I get one. And the third image, wrong. And the fourth image, correct.  So we, they upload the four documents at four times and we need to run the processor four times. There are four exfusions.  Well, we could tell the user, okay, instead of upload one document. document at a time, can you upload four documents together so we can we can do we can do that but what if like a user insists to do this one by one okay another scenario is we already have four files there and they decided okay I want to remove two of the files and I want to upload two more or like I want to overwrite two of them.  and since the overwrite can only be done one by one how can we design a schema that is able to minimize the number that we run the procession.

1:34:50 - Jude Pineda
  How about we validate the uploads first June like we require for owner one we require the front and back two separate fields so that they can upload one they have to upload both for that owner and if they want  If add another owner, they just have to pick a button there, and then another two input fields will be there, so they can another upload for the front and back for that next owner.  And if that's missing, again, it should be validated from the front end first, so that no unnecessary executions will be called later on.

1:35:24 - Chun Shao (Simple Code AI)
  Okay, so Adrees, is that possible that they validate the documents, everything in the front end before they hit like an update or save button?  So what kind of validation? Maybe just a required field.

1:35:41 - Jude Pineda
  We don't have to check if it's a valid driver's license. First, we just have to validate if that specific file upload is filled.

1:35:52 - Adrees Muhammad
  Okay, so these kind of validation, document-based validation, I think we need to perform the OCR for that. Let's say, but let's...  Let's say we have in a driving license, we have four documents, two documents, front and back. So we can validate that part before we perform the processor execution in maybe in a document processing module to check if we have the back and front.  If we have, then we perform the processor execution to optimize that thing. So that's one part of the validation.  And for the other application form, we can do that to enforce the required feeds in front end itself.

1:36:47 - Chun Shao (Simple Code AI)
  Okay, so this one should be easier to handle. Okay, like for the others, I think you can allow the jack and the job multiple files at a time.  Okay, so be Okay. Put some like a preview possibilities, allow them to choose the stabilization type, and then hit the submit button, so you will receive all the documents along with the application form that are all in once.  Okay, then this will not like create too many executions for the processor. Also, for the like update of the documents, once they upload it like for bank statement, it's fine, it's like each document based, so you delete it, you update it, it won't affect a lot.  It's only like for one particular stipulation, okay, if you, if you need to do any change on the documents, it's still acceptable that, like you delete it or, I don't know, this is not a big issue.  Okay. It's fine. But here, when we talk about this activation, we want to combine all the operations into one.  Okay. We really want to do that. And how could that be implemented? So Adrees, you mentioned that you created two different kinds of functions.  One function, where every message, one function was not, right? This is what you're talking about. Yeah.

1:38:42 - Adrees Muhammad
  So it depends on the design of Jude as well. Like if you want to call the base functions, in between the business logic, then it can become a problem, but I don't think so.  Because we have defined that these specific functions will only emit the emit, and we will only, and Jude will only call those functions when they need to emit.  I guess we can handle that.

1:39:17 - Chun Shao (Simple Code AI)
  Yeah, probably that is the easiest way. Okay, so for our data module, every function, you will have an indicator whether emit message or not.  So they can control, like a, Jude can control, okay, this update of the, of the documents or the application data will not emit messages.  So it won't become a loop. And then in this case, you need to handle the consolidation by yourself. Right?  Yeah. Yeah. Okay, then this is, this is the simplest way to start.

1:40:03 - Adrees Muhammad
  Because we have defined that these specific functions will only emit the emit, and we will only, and Jude will only call those functions when they need to emit.  I guess we can handle that. Yeah, probably that is the easiest way. Okay, so for our data module, every function, you will have an indicator whether emit message or not.  So they can control, like a, Jude can control, okay, this update of the, of the documents or the application data will not emit messages.  So it won't become a loop. And then in this case, you need to handle the consolidation by yourself. Right?  Yeah. Yeah. Okay, then this is, this is the simplest way to start. With it. Chun, can we do that, like, in front end, as you said regarding the validation, as we know, in driving license, we need back in front.  What if we just auto-classify it in front end while user upload it, like you mentioned that in previous meeting?

1:41:32 - Chun Shao (Simple Code AI)
  Let's say user upload documents, so it just didn't click the create and writing yet, just upload those documents. We are creating the signed URL, but we can perform the OCR at that, or classification at that point as well.  So the classification will give us results. Maybe this document is the front of the, maybe driving license, or this is the back.

1:41:58 - Adrees Muhammad
  And if the user just upload one document, we can just add an alert, or a...

1:42:03 - Chun Shao (Simple Code AI)
  Notify that user, we should need the front and back of that driving license. So in that case, we can reduce that part.  Like if he, in first creation, he just upload the front and in second creation, he just upload the back.  So we can handle that part. In that case, if we perform the auto classification in the real time. Okay.  It's possible. First, it's possible to do that. Second, is this classification cost money. What if they do the classification and didn't upload?  So we will not be able to check it because it's all happened in the front end. Are we using any LLM in the classification?  I think we have our own model. Yeah, we'll have a amount of, but even use LRM, you still need the cost for the consumption of LRM model tokens.  Okay, yeah. Yeah, so. Yeah, so like, so it's like we, okay, for now, I checked with SD, this is interesting.  So if you provide a document, let's say it's an image file, okay, and if you don't do the OCR, you upload the image file, we're using like a LRM, LRM cloud to do the classify.  Okay, it's very good. So far, we tested the performance is almost perfect. Okay, so let's say we use LRM cloud, do the classify.  Here is the charge now. The person will charge one. Credit per page and the classified, which is better version, but now it's free.  Okay, that means, and you can specify like, to do the classification, how many pages, maximum pages you need to do to parse.  So let's say if we set, okay, we do five pages and we upload the file and we, it's a PDF and it's images.  We didn't do OCR and we upload the file to them directly, so it will charge five credit, which is half cent to do the classify, because the classification doesn't charge for now, it's a better version.  Okay, if we do the OCR and save it as an OCR file and upload it to do the classification, actually there's no.  But in the future, I don't believe that the classify of Lama Cloud will always be free. So in the future, it will start charge some money.  Okay. And then we gonna need to charge the client who using our system for the classification, but we can tell them, okay, so if you don't have a great amount, and you know the stipulation type of each document, you can manually tell us what's the stipulation type of this document, and we'll save some time to do the classification.  And we can also save some costs to do the classification. So that's why we allow them to choose the stipulation type.  Okay. To create a underwriting. Thank But we keep the function, like a classification, be possible so we can streamline the whole process to be automated to get a suggestion if they provide enough documents for us.

1:46:21 - Gene Rellanos
  So this is why I think, okay, why we don't, and also it takes some time to classify 10 documents.  Yes, it will take maybe one or two minutes to get all classification information. Okay. So it's not very fast, it's like, not like you upload a file and the backend classification can give the classifying in a couple seconds.  No. So for each document, it could take maybe 20, 30 seconds. Seconds, or 10, at least 10, 15 seconds to get it to be classified.  More or Salori? I have a question for the classification. Do we just drop it in one place? Like we mix the different files, like bank statement, driver's license, and just dump it to one input field?

1:47:33 - Chun Shao (Simple Code AI)
  And the AI will classify all that, or we separate them by, let's say, for this field, it's only for driver's license, and for this field, it's only for bank statement, and not being able to do then.  dump it in one place, and AI will be. yes, yes. Yeah. I see. But if we do that, how can the AI maybe match the driver's license button back?  Yeah, good point. How does it know that this, for this driver's license, this is the back image? Or is it that the driver's license is in one PDF file, like front and back already?  Like there's two pages in a PDF file, and that PDF file contains the driver's license, first page, front, second page, back, so that this is going to be the handle of the processor in detail.

1:48:42 - Gene Rellanos
  Okay, so basically it's like we get an image, and we get all the information, and we extract the data from this.  Okay, and maybe we will compare all the data returned by each document. Either it's an image, or it's a PDF.  So some image could also contain like a back, front and the back. Okay, some image only contains front, some image only contains back.

1:49:15 - Chun Shao (Simple Code AI)
  So before we like generate those factors based on the output data, this is what we call a consolidate station we'll do is trying to refine the data, the output data we get, and try to match any two that are likely for the same person and then generate those factors.  Sweet. Yeah. And some extreme scenario maybe, let's say the bank statement for February for that month, let's say it's too long and it's too, maybe it's an extreme case, maybe it's too long and it's split into two files.  think. was situation you is is huge big

1:50:03 - Adrees Muhammad
  How do we know that this bank statement is just for February's two files in it? But no, we don't have a way to handle that.  We have to ask they to upload another file, to combine these two to one and upload it again. I see, I see.  But that's an extreme scenario, maybe, you know. Yeah. Just the, yeah. Yeah, what is correct, like, we have seen this one scenario, it's like, we ask you a bank statement, and the user provides six, seven different screenshot of his cell phone.  That's the bank statement. Okay. Yeah. It could happen. It can happen. Yeah. At least. Yeah, Chun, so as you said, we have a cost to classify the documents.

1:51:12 - Chun Shao (Simple Code AI)
  We are currently, we are concerned about the, let's say, driving license or those documents which required multiple or those stipulation types which required multiple documents.  Okay, so what if we, because, and those documents will be, will be uploaded by the user separately one by one.  Okay, and they will have one page. What if we just suggest the stipulation type of those documents which, which only have one page.  Because, the bank statement will have multiple pages and we don't concern about bank statement. just execute the processor and just, but we are concerned about the driving license.  Let's say we have two documents, but the one execution. So we can just predict or manually classify those documents which only have one page.  It will cost us the minimum and we can... Well, yeah, the classification is actually very, very, very cost-effective. I can show you the classification.  Okay, if you allow me to share the screen. Sure, okay. Yeah, and you can have an idea of it.  This is Lama Cloud. You see it, right? Yeah. Yeah, I see it. Okay, and you see there's a classified beta there.  Okay, so what I need to do is like a... It'll give you some like a predefined rules. Contract, resume, receipt.  So we will see it defines the type and the description. That's it. Okay, describe what kind of... It's a contract, a legal agreement between parties online.  Okay, so what you will do is you just drag and drop files, and it will do the classification. And I can show you the history.  Oh, I don't have anyone here. I don't have any history. Do I use anything? Oh, probably this is on another account.  Okay, let's do it right now. Okay, more templates. So they have like a bank financial, they have bank statements.  Okay, so what is bank statements? It gives a definition. Okay, and I add one. Driver's license. Okay. Okay. government issued ID and...  A government issued. issued. issued. Education document for, document for driving and personal, I, I don't know, okay, for driving, all right.  It includes name, address, date, birth, gender, and, yeah, gender and other information. Okay, so, so what we need to do is, let's try to find some example documents.  Hold one second. Let me just find all the folders. Yes. I have a driver's license. Okay, we can see this is.  the driver's license, and I pull up a bank statement, okay, okay, I need to pull up a bank statement, so we have a bank statement, I can pull more data, like a signed contract, okay, I put a contract, so I add a contract, so I will have three, okay, and I have three documents.  All what I need to do is classify it. All right, and you can see it's very fast and convinced.  Again, it gives you the reason, okay, why this document, a driver's license, okay, contains separate single letters, just numbers, you know.  Okay. No financial records because you just give these three types. Okay. And so actually this is not very, no, this is not good.  This doesn't match. So that means the OCR has a problem. All right. With the pricing. And this one is a hundred percent with a bank statement.  Okay. Contains everything. And this one is a contract. Okay. A hundred percent. Contains contract everything. So if you look at the usage.  And you can see there are 11 pages past. This is because the contract. Let me check how many pages I have.  So, hold on a second. Oh, a second. Oh, 13 pages. But it will only take the first five, and Java's license is only one, and bank statements, let me check how many pages I have in total, 10.  So it's like two documents use the five page, and Java's license use one page. Okay, but this is not a good result because Java's license doesn't recognize.  So what we will, what we can do is probably we can, let's say, we edit because the direction of the Java's license is not correct.  So let me edit it, and move it, like rotate it to the correct position, and save it again. All right, and let's do this again.  So how I can start over, no, not start over, I have this, and reclassify, no, this is just doing the same job.  Hmm, I cannot pull up the... Oh, actually I can edit this, but I cannot edit the file. Okay, I can only edit the rules.  Okay, let me copy this rule. Alright, and let me check the usage, delete, create any extra usage. Well, it's still 11 because those documents has been...  Passed already. So let's go to Classify. And we have a bank statement. We have a contract. And we will have a driver's license.  Okay. And then let's do this file again. Okay. Along with the other two files, which is bank statement. Okay.  And contract. Let's classify it again.

1:59:57 - Gene Rellanos
  Okay. Now it recognizes this as a jealous license. Okay. With all the information extracted.

2:01:03 - Chun Shao (Simple Code AI)
  This part, SD already taking care of it, so I told you that we won't do the OCR. We're not allowed, okay, we will not upload the image directly, we'll do the OCR.  So if we do the OCR for one file and get not good result, we rotate it, okay? And until we find a good result for different rotations, and we use this result to upload it, to classify, it's much accurate, then we do the classification directly.  Yeah, we will, we will, we already handle this, yeah. Okay, so Adrees, so for your suggestion that, I would say for now, we, let's do it in the backend, so we can keep the track of everything, and check the cost if necessary, okay?
