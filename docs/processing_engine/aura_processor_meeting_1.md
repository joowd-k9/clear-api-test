Oct 1, 2025
AURA Processor Design - Transcript
00:00:00

Gene Rellanos: Good morning everyone.
Chun Shao: running. Okay. Okay. J. So, let's look at the updated document. Okay.
Jude Pineda: Okay.
Chun Shao: Yeah, sure.
Jude Pineda: Uh would I be sharing my screen? So uh for the execution I added uh uh use case uh as you asked uh yesterday. We have here uh for clear person search. Oh, it will be executed uh when using a concurrency.
Chun Shao: Okay. So for clear person search. So this uh concurrent processing.
Jude Pineda: Oh yes. Uh so first we we transform the owner list into two items.
Chun Shao: Mhm. Mhm.
Jude Pineda: Uh extract which is extracted from the orchestration message and then uh and then it will be validated.
Chun Shao: Okay.
Jude Pineda: Uh so after the validation the base class will handle how this uh extraction will be run using this red runner which will be run concurrently uh independently independently with owner A and owner B and then we aggregate the
Chun Shao: Yeah.
Jude Pineda: results then validate and so after it passes all that steps so we have to persist it to database and update necessary application form fields in the underwriting.


00:02:52

Chun Shao: Mhm.
Jude Pineda: Then we end the execution and there's also uh for bank statement.
Chun Shao: Okay. Okay, good. Yeah, this that's
Jude Pineda: Um so uh so from the bank statement uh since we receive a list of document ids uh this is just a use case example. So uh and then we chunk it by months. So and then we validate it just means uh it just means that we split or splice the document by individual months.
Chun Shao: okay. Hold one second. So, uh, transform bank statement split by month bucket. What does that mean? No, the the document provided is already monthly based.
Jude Pineda: Oh, so if that's the patient then there's no more need there's no need to split. So we just run return it uh individually here and then we validate each uh document here if there's uh additional validation needed and then for that individual uh documents uh we run that concurrently.
Chun Shao: Okay.
Jude Pineda: So yeah and then we aggregate all those individual results like getting the average uh trend or something like uh the NSF's total amount uh total count within the six month period for example


00:04:27

Chun Shao: Okay. Yeah, this is this will be very complicated. Okay. Uh but uh like at the pre-check of all the documents, it's like a you can you can uh upload okay to the document parser which is also written by us um by uh like each file individually directly submit to them. Okay, they will process and return the result. So with the result returned they have like a beginning date, ending date, beginning balance, ending balance and you need to aggregate this part is uh the most difficult part for this processor because it need to aggregate the result and probably will also use some part of AI to find out uh certain things. Okay, it's like uh it needs UI to find out the potential maybe the loans they have currently. Okay, the position uh by um trying to find this uh pattern of uh uh regularly payment especially those a processor payments. So this this can be uh found from this uh uh descriptions of all the transactions. Okay. And uh you also need to do some calculations.


00:05:53

Chun Shao: Okay. If the let's say um if the if this uh uh banks uh statements like uh they have uh uh debits they have credits and for the credits it's like uh you you have like um uh income and uh uh how to like uh identify those incomes which can be counted as like the revenue. Okay, some income may not it's like a transfer from account to uh from one account to another account. Uh but some it's like a regular income either from a like Amazon sales or from their store sales. Uh this kind of things we might need AI's help to find this information out. uh but uh yeah but basically like we can improve the processor gradually okay uh all right and uh now I ask one question is we haven't test this document parsing thorly uh let's say what if we need to review like the data parsed is not reconciled okay that means uh the beginning balance any balance and every transaction if you add the numbers together they don't match. It could be like a there is um missing of one or two transactions in the list or it could be like a um OCR recognition error or it could be involve other uh non-transactions uh record into the transaction.


00:07:43

Chun Shao: um what we going to do with that? So this is not a simply like a failed pro execution. Actually it's it's executed. We just need like a review. So think about this. Maybe we should add like a this is uh special um we should add like a review of this um processor especially this bank statement. Okay. Uh reveal the route that uh it accepted and we can uh be able to like change it. Okay. Um yeah, for for this part, this is like a special part. Uh we may think of it um you can you can talk with uh Adris and uh or like a attic. attic is more uh familiar with because he's working on the front end of this document processing. Okay. And he's like doing this u uh like a adjustment the modification in the front end. Okay. And uh in the beginning I was asking address uh like to write this uh front end uh as a component that they can review.


00:09:07

Chun Shao: Okay. They can make any modifications to make it as a reusable component. I don't know like how much it can be reused in this case but uh yeah this this is what we need to talk with um Alli. Okay. Uh, regarding this bank statement, in case there is any, you know, errors, they can review the result and fix it. Okay. J, you understand what I'm talking about?
Zhanfan Yu: Uh yeah but I have one more questions.
Jude Pineda: Oh, yes sir.
Chun Shao: Yeah. Yeah.
Zhanfan Yu: Uh I think this design here I mean if I understand the uh if I understand this correctly that the design here that you you should uh design the uh abstraction that uh all processors will follow or steps that all processor will follow but not specific to a bank statement processor.
Chun Shao: Yeah.
Zhanfan Yu: So like uh cuz for for other processor that uh like uh passport or other processors they might not need to split by months.
Chun Shao: Is it
Zhanfan Yu: So the procedures here should be like generalized to all the processors that they need to follow.


00:10:32

Zhanfan Yu: And this uh to me is more like specific to bank statement processor.
Jude Pineda: Uh this is just an example use is actually we can always uh do whatever processing logic we need during a uh in the transform wait uh in the transform method right so
Chun Shao: Yeah, Jeremy, this is what I asked uh Jude to like a use one or two example to demonstrate because I I I cannot understand the runner idea but from here I I I can understand the idea of the runner. So yeah, this is uh because I asked yeah give an example but uh at the meantime you should have like a common uh workflow. Okay. And uh you can yeah you can then you can list like uh what is the pre-check and for like a document uh parser or like a document bank statement uh processor what's the uh like what's the review okay
Jude Pineda: f***.
Chun Shao: uh preview and uh well what is the runner difference of this uh thread runner or like a uh sequential default runner. So yeah. So yeah.


00:11:44

Zhanfan Yu: Yeah.
Jude Pineda: Okay.
Zhanfan Yu: Yeah.
Jude Pineda: Yeah, I'll add another example too.
Zhanfan Yu: And yeah. And also I think for specific like processor you don't need to use parallel. I mean it will just increase the complexity. you can just uh extract the factors uh I mean in a cascade way or sequential way you don't need to do do it parallel yeah you you no no uh go back to the uh the bank statement example
Jude Pineda: Uh yeah. Yeah, we have the default here. Yeah.
Zhanfan Yu: yeah uh so what I mean by uh you don't need parallel here is that you don't need parallelism and uh you can just extract the uh the months one two three and in cascade way you don't need to do the parallel in specific processor again because you already have the par uh par parallel uh or parallelism in the uh with executing the processor so you don't want to over complicate your problem uh within the processor you see what in. Yeah.
Jude Pineda: Yeah, I got Yeah, I got your uh answer.


00:13:01

Zhanfan Yu: So for this one probably uh just need a pre-check and then extract all the factors from bank statement uh in a sequential or cascade way and then you don't need to uh do the parallel and you don't need to uh aggregate the result. it'll be more uh clear and then for the processor level that you can do the um parallel and then aggregate the result I mean for the processors because you're going to have a back segment processor you're going to
Jude Pineda: Oh, what was that again? I'm sorry. The last part.
Zhanfan Yu: have other factor processor and then for that you probably want to use a parallel and then aggregate the result but within the processor uh you don't want to do the parallel effect.
Jude Pineda: and so yeah so my plan was to uh to execute processors uh using multiprocessing uh but uh but for the inside the processor itself uh they can always have an option to run those uh concurrency using multi- threading So yeah there's a different level of multipprocessing for different uh processors itself and then and multi- threading for the processor execution.


00:14:22

Zhanfan Yu: Yeah. So that that is what I'm saying that within the processor itself that it does not need the parallelism.
Jude Pineda: Ah okay okay yeah I got it.
Zhanfan Yu: Yeah. Because it will over complicate problem. you already have the all uh parallelism um for each processor like when you're running all the processors you already have the parallelism and then so that within each processor you don't want to do the parallelism again
Jude Pineda: Oh yeah. But it's up to uh it's always up to them how to uh if they want to implement this or not. I will update this for uh I will add another example for this uh for a simpler one uh as you as
Gene Rellanos: So I guess the the parallelism shown here in the uh processors are just an example. So we don't so we don't have to follow exactly what's uh in the diagram. So it's up to the developers. Is that what I'm understanding?
Chun Shao: Okay. So like what uh Jeremy's suggestion is uh like we can simplify the design.


00:15:32

Chun Shao: Okay. So um let me still use this two as example like a bank statements. So um so in the like processes like you received the popsup message and you might generate uh like a create five uh processors. you find out okay these five processors need to be executed and uh instead of like for the bank statement you only create one processor and run it in the thread um you should determine okay how many like if they there are three documents need to be processed so you need to create three threads for the bank statement processor okay and run them simultaneously ly. So for each processor, it will only handle one bank statement, right?
Jude Pineda: So if that's the case uh do you mean by one bank statement uh is that is that one month for example but how are they going to aggregate those results uh if that's the This
Zhanfan Yu: Yeah.
Chun Shao: Uh-huh. Yeah. Yeah. One month. Okay. So once you get the result okay you will go to the database to find out all the existing okay result and update it.


00:16:56

Jude Pineda: so that's another uh layer I think
Chun Shao: Yeah, like let's say this, okay, in the beginning, you don't have any factors of monthly revenue, okay? Because you don't have any uh bank statement processes execution. And now you received the three documents, okay? And you create three threads for bank statements. Okay. And they they're not complete at one time. They completed uh at multiple times. Okay. And when the first document is uh executed finished all right the monthly revenue will be based on the data that is for that month. Okay. So let's say it's like a $10,000. All right. And then after after like a couple of seconds the second bank statement execution completed. So and the second the monthly revenue according to that bank statement is 12,000. Uh so the average will be 11,000 instead of 12 or 10 because now you have two and the average uh monthly revenue is 11,000. And then you receive the third one and the execution ended and the monthly revenue uh for the third bank statement let's say it's um maybe like uh 8,000.


00:18:26

Chun Shao: Okay. So um from the previous two which is 11 and the third one is 8,000 you get an average to be 10,000 monthly revenue. Okay. So the like the aggregation of the data is not only like based on the data it has it's uh but instead you should like include the historical executions of this particular type. All right. Mhm. And this could be like avoid uh the flaw like maybe in this design of processor executions that you put everything into one process and the result is only based on this documents. So what if they only upload uh what if they upload another extra document into the system and you will only process that document update factor that's not correct. So in this case, so each processor execution uh there is only one um uh like a uh one one execution okay one document or one person uh but when you do the aggregation of the data you should consider the history
Jude Pineda: So uh judging uh from what from my understanding of this uh design by address I think that will break this decision uh because I have asked them what if we delete the bank statement.


00:19:59

Jude Pineda: So if that's the case uh those calculations that are included in the historic uh calculation will I think will break the factors being generated by that specific execution because it is basing previous uh stipulations right like let's say
Chun Shao: Sorry. Shut up.
Jude Pineda: for the month of March and then we process uh April's uh bank statement if we delete March then the extracted factors uh for that period in the April uh it's not going to be correct. That's the case because we're including the previous result execution and we're also uh calculating it for the factors of uh April bank statement.
Chun Shao: Mhm.
Jude Pineda: Yeah, I think it's going to break the design here.
Chun Shao: Well, uh the only case I would think of like a break this is for example they have a pre-check criteria. Okay, for the factors no problem because they save the history of the factor. So like for the monthly revenue the factor will have three different values.
Jude Pineda: Mhm.
Chun Shao: The first one as I gave the example the first one will be 10,000 the second one will be 11,000 the third one will be 10,000 again okay so it's it has three different values okay um yeah there could be a potential error is that if they set up a like a pre-check function and uh let's say if they say okay if the revenue is uh less than 10,000 I will reject it and uh what will happen


00:21:50

Chun Shao: is like uh the lowest monthly revenue which is 8,000 is finish execution first. So this factor will become 8,000 first and then the pre-check will rejected. All right. The status of this uh application will be rejected. Okay. But um I mean uh it can be adjusted because later on because the factor has been changed even though the first one is 8,000 for monthly revenue but after the second uh bank statement has been passed for example if it is like a uh 12,000 so it will bring it back to average 10,000 and it will not be rejected. So it will be passed for this criteria.
Jude Pineda: Uh so from my understanding uh individual stipulations will have a mult uh so a stipulation can have many factor keys here uh for for a single execution.
Chun Shao: Okay.
Jude Pineda: So I think there's no I yeah it will override in some way but my concern there is for the deletion part of us it's certain stipulation if we use a previous uh for the bank statement if you use March for the calculation of like let's say NSF for that period then it's going to break it's not going to be correct in some sense let's say that also


00:23:22

Chun Shao: Yeah, even though even though it's has its execution ID but when you generate the factors you are not only based on the data from this execution you should based on all the historical data of this uh bank statements. You understand?
Jude Pineda: Uh yeah I understand correctly. I am just concerned with the delete stipulation deletion and the actual correctness of the factors being uh saved in the database.
Chun Shao: Yeah. Uh can you say that again? You're concerned about what the stipulation.
Jude Pineda: Let's say for uh March, April, May uh bank statements uh if for that individual executions uh it will uh say save many factor keys here individually.
Chun Shao: Mhm.
Jude Pineda: So let's say uh NSF count for March we have five and for April we have another five but if we include a historical data so do you mean like we we save it uh as 10 for April because if that's the case if we use 10 to save it under the bank statement of April then it's going to be uh there's going to be a problem if we delete the March period.


00:24:34

Jude Pineda: So because in April we only have five but we have stored 10 because we included it included the previous uh result.
Chun Shao: Sorry, Jude. Can you say it slowly? Uh I understand you give me try to give me an example for March, April and May and I didn't get the numbers what is 5 10 I I don't know if there is what
Jude Pineda: Yeah. Uh yeah uh if there's like an non-sufficient fund count of 10 during March I five I'm sorry uh NSF factor non-sufficient fund yeah for month
Chun Shao: factor non non-sufficient count factor.
Jude Pineda: March for March.
Chun Shao: Okay. So you're talking about non-sufficient fan fracture. Okay. Yes. And then for March.
Jude Pineda: Yeah. So if we go to April and we found another five, so that's going to be 10, right?
Chun Shao: Okay.
Jude Pineda: Are we going to save 10 or are we going to save four for the i5 for that April?
Chun Shao: Yeah.
Jude Pineda: Because if we're going to save 10 and we delete the previous stipulation for the March, then it's not going to be correct.


00:25:31

Chun Shao: Okay. Okay. Uh hold one second. uh it depends on the definition of NSF. If it's cumulated then it will be 10. If it's average NSF day per month then you should do the average.
Jude Pineda: Yeah.
Chun Shao: Okay.
Jude Pineda: Uh either way J it's going to be incorrect if uh either way if you're going to aggregate or do average it's going to be incorrect if we delete previous stipulations for so either way June so let's say four
Chun Shao: So which one? So which one you're talking about? Which one you talk average or accumulated?
Jude Pineda: and five so if we if you do aggregation that's going to be nine and if we're going to be average that's going to be 4.5 but if we're going to delete again the previous uh stipulation like March I'm
Chun Shao: So yeah. Oh, hold on. You're too fast. You're too fast.
Jude Pineda: sorry.
Chun Shao: So now Yeah. Okay. So you say, okay, now I understand. Uh let's say these two factors average is 4.5.


00:26:36

Chun Shao: The other one is nine.
Jude Pineda: Yeah.
Chun Shao: Okay. Now you are talking about you want to delete uh delete march.
Jude Pineda: The March. Yeah.
Chun Shao: Okay. So okay this is uh this is this is not what we are. Okay. So this is different from what we previous discussed. So this is about deletion.
Jude Pineda: Yes.
Chun Shao: Okay.
Jude Pineda: Uh so we have to maintain the actual correctness of the information that's being stored.
Chun Shao: Yeah. Okay. Yeah. Yeah. Yeah. You're right. If there is a delete document like this is update. So yeah it will be a like a the deletion of the previous execution. So it's not only like a execute but actually it will remove the records of previous execution. Okay. So it's like a mark this execution as uh deleted. Okay then what's the story?
Jude Pineda: I'm I'm talking about uh deletion of stipulation uh as uh since I'm sorry delete ing a document screen


00:27:37

Chun Shao: delete a stipulation. A stipulation cannot be deleted. You only can delete one document. You cannot delete a stipulation. Okay. So yeah, let's say you delete documents. Then what will happen?
Jude Pineda: since we're basing uh the result of that document to another execution. That's and if you delete that document that there's going to be a problem later on
Chun Shao: Okay. So if you delete the document because in the design we don't have like a deletion be considered here deletion of a document. Okay. We include like in the update. So update means like uh we only concern about like a new document but what you're talking about is like we remove the document. Okay. So this is like a you need to handle that separately. So not only you will listen to creation, not only listen to update, you also need to add another popups message which is delete.
Jude Pineda: uh yeah from our discussion with address.
Chun Shao: Okay. Yeah, you you make a good Yeah, you make good point that you we need to add one more uh message is the delete.


00:28:54

Chun Shao: Okay. Now let's talk about the delete. If there is one document deleted okay and for example that is a bank statement. So what we need to do is we need to delete the previous like execution result or at least mark it as uh deleted. Okay. So it will not execute it will not call like a run it again. But it will be marked as deleted and the aggregation operation will then rerun. Okay. And uh yes and the factory will be updated. Okay. and uh will be updated and with this underwriting processor uh no with this execution ID the deleted execution ID uh and the value is uh the updated so let's say if you previous is four and the second is five so average is 4.5 then you delete the document which gives you the five then the result will come back to four again, right?
Jude Pineda: All right.
Zhanfan Yu: Yeah, I think that um so like uh no matter we have delayed or not uh both method should give us the same result.


00:30:11

Chun Shao: Yeah.
Zhanfan Yu: I mean the the method that you're proposed and the method that I I wanted to simplify should uh both be the aggregation result at the end so that uh even though that we do the deate so both uh both me method should give us the same result at the end so yeah do you see what I'm uh what my point Yes.
Chun Shao: Yeah. So you do you have any question?
Jude Pineda: Uh, I'm sorry, Jeremy.
Chun Shao: Are you clear now?
Jude Pineda: I still I I didn't get it.
Chun Shao: Okay. So what what's your question like let's say okay um we have three bank statements as you said March, April, May okay and we process one uh n of day is four days okay and we have a average factor which value will be four okay this is the first execution the second execution we get another mouth and it's five Okay, then the aggregation operation after the execution will uh create another record of this factor and change it to 4.5. Okay. But these two factors actually they share the same factor key and they share the same uh underwriting ID except they have different ID but the second one if you look at your screen will have a super seed ID which indicate the what's the previous factor.


00:32:10

Chun Shao: So the previous will be four and uh the most updated current one will be 4.5. All right.
Jude Pineda: All right.
Chun Shao: Okay. Yeah. And uh well uh anyway I okay this is I can discuss with address. Okay. I don't like the idea of this supersedes ID. I like the idea of the like not super like the updated ID. Okay. So in this case we can uh more fast to locate who is the most updated uh factors. Okay. you don't need to go through the whole chain and what if the chain is broke. So as long as the updated ID is now this is the most upto-date value and if there is any new factor uh being generated like a new value of this factor being generated first it will find is there any records and if there is then find out who's like a the updated ID is now and create a new record and update this one update the ID to the new ID. So in this case I think it will be easier to locate the most up to date.


00:33:25

Chun Shao: Okay, this is uh extra. All right, let's come back. So now this factor comes to 4.5. All right, then uh before the third one uh being passed. Okay, the underwriter manually deleted the second document which is five. Okay, he said okay this is not for this client. this is some other client's document. I upload the wrong uh document. So he delete it and uh uh this delete will uh generate a new popsup message which is not handled here but in the future we'll handle it which is delete the second document and then it will go to the uh database find out okay do we have any execution for the second document? The answer is yes there is execution and uh what is the most upto-date execution uh of it uh and then mark it as deleted or mark all execution as deleted. So after that it will do the aggregation again. So this aggregation actually is independent to uh any like a document. So the aggregation is like after you run the execution you save all the uh output result in the database.


00:34:52

Chun Shao: So you from the database you can find out okay uh there is only one uh valid execution now because the second you delete it and the factor should be four again. So now there will be four uh three factor history. The first is uh four. The second is 4.5. The third will come back to four again. And then the third document execution has been finished and it returns a value of six. Okay. And this factor will be aggregated and generated again. So the fourth record of this factor will be five because it's the average of four and six. Okay. And after a while uh they said, "Oh, I wrong. I I like mistakenly deleted. Okay, it should not be uh like deleted the five. So they undeed. Okay, they undeaded. All right. And do we like if we can handle this well and we say okay this this document we have execution and uh now we update it because it's deleted.


00:36:03

Chun Shao: So we don't need to run it again. So we just recover mark this deletion as an undeated and we will reagregate and recalculate the factor again. So the factor will still be five but this five is based on three records four five six. Okay I didn't see any problem here that will create because of this design. Do can you think of any possible problem as long as this aggregation is based on the historical data in saving the data warehouse. is not based on the data by the execution itself. Okay.
Jude Pineda: Yeah, I think we we'll be breaking the Iden potency uh here.
Zhanfan Yu: All
Jude Pineda: So because if we only run April without March, it's going to yield a different result than comparing if we run it with March.
Zhanfan Yu: right.
Chun Shao: Okay. So like you need to change the idea that uh running April without m March. Okay, running April is independent to March.
Zhanfan Yu: Yeah. So I want to clarify that uh this processor uh will be like transactional as trend described.


00:37:31

Zhanfan Yu: So which means that no matter whether a user delayed or delayed a file or not it will run it all the executions. Let's see that uh before the user delayed it has five months or it has three months one two and three it will aggre it will run all three months and then aggregate the result no matter what happened.
Jude Pineda: Oh, okay.
Zhanfan Yu: So even even even though the user delayed the month two, this three file will be like still run first and then aggregate the result then the user will delay the months two instead of like we terminate or interpret
Jude Pineda: I got it now.
Zhanfan Yu: uh we pause the system to delay the file first and then continue doing the aggregation.
Jude Pineda: So yeah, I got your point, Jeremy. Uh it's just that from our previous discussion with address uh when there's a stipul uh when there's uh deletion in documents uh uh he's going to handle it like delete all the factors that's being inract extracted with that specific documents etc. And for my end uh we have discussed that it's not going to uh to be reached to the processing engine.


00:38:47

Jude Pineda: it it's like it's going to end that document uh data collection.
Chun Shao: Yeah, there is what you want to
Adrees Muhammad: Okay. So, regarding the deletion part, uh I thought like to add a soft delete like we we should not delete the document from the database. We can just add a property here and uh using that property we will uh do the rest of the logic like uh if the document is deleted then we should not uh uh use the factors against that or the uh other details associated to that. So, so that's Yeah.
Chun Shao: Yeah. Yeah. So if there is a docu document deleted uh the execution relate to that document will also be soft deleted marked as deleted and the result will not be considered in the generate of the factor. Okay.
Adrees Muhammad: Yeah,
Zhanfan Yu: Um, but twin I I think that uh Uh yeah. Uh let me I I think that uh we we market soft uh delayed but the uh but we still need to aggregate the result again cuz like Yeah.


00:40:24

Chun Shao: Yeah. Yeah.
Zhanfan Yu: Yeah. Yeah. Yeah. Yeah. Yeah.
Chun Shao: Yeah.
Zhanfan Yu: So yeah because it it's like um we first uh finish one transactional operation to get all the result uh factor result um and then we we market the late and then we need to aggregate the result again based on the uh this update. So yeah.
Chun Shao: Mhm.
Zhanfan Yu: Yeah. Right.
Chun Shao: Yeah. So actually for each different processor uh it will have a aggregate. Okay. And this aggregate is just based on the processor. It's not based on the execution. You understand what I'm talking about? The aggregation is based on processor. It's not based on execution. So on another hand it's like no matter what kind of data what kind of result yield from this execution the aggregation result should not like a solo relied on the execution result it should rely on the database. Okay. So the execution the end of the execution is the data recorded in the database.


00:41:47

Chun Shao: Then you run this aggregation. So you can even like run this aggregation even without any execution like the case you just given uh as you delete a document that will uh that will introduce a delete of execution. So actually there is no new execution there is just a mark as this aggregation or this execution as deleted but this will result in the re calculation of the factor and this aggregation is independent to the execution. Okay it's only related to what type of processor it is.
Jude Pineda: Um, yeah, I understand actually, but I think that's more complicated to implement than running all uh all of those in a single execution.
Chun Shao: You think it's more complicated than what?
Jude Pineda: I think it's more complicated than just uh running that in a single execution.
Chun Shao: Then just running what?
Jude Pineda: running those uh six uh three bank statement in a single execution.
Chun Shao: Ah okay. So you are still thinking of like a Okay. I I understand that if you take this three execution as one running and only do this aggregation after the running, right?


00:43:25

Jude Pineda: I don't get it. I'm sorry.
Chun Shao: Yeah. So like what you said what you design is you have three execution and only one aggregation. Am I correct?
Jude Pineda: Oh, no. Uh.
Chun Shao: Instead like our design is uh three execution and three aggregations.
Jude Pineda: Oh, yes. That's what
Chun Shao: Yeah. Yeah. This is what Yeah. This is the the main like a difference between our designs, okay? And uh uh I I'm trying to persuade you, okay, that this design seems like you have two extra aggregations, okay? Looks like this is like a not as efficient as your design that you have three executions but only run this uh uh aggregation once. Okay, let me explain why this is uh this is uh more this is better design. Okay. So, um in your design is like uh this uh this this processor is um you have like a can handle multiple documents. Okay. The pro part is yes this aggregation can wait until all three documents has been processed and you can do that.


00:45:00

Chun Shao: Okay. And uh the the the uh the cons part of this is um when you do that this is based on that your aggregation is only based on the execution results either one execution or two execution or three executions. You forgot the historical data. Okay. or it could be forgotten the historical data that need to be included in the aggregation operation. Okay. So actually in whatever design you should always go back to the database to get the historical executions and combine with this three executions and do the aggregation. Okay, this is this is very uh easy to be ignored in your like a design here. So this is why uh Jeremy and I suggest you like uh to keep execution and aggregation uh independent with each other. So in this case we don't need to like a wait like this uh so for each execution their aggregation is independent to the execution. So no matter which one finish first and even there is like conflict among the factors. Okay like uh this processor will update this factor another process will also update this factor.


00:46:41

Chun Shao: So uh actually they are all based on the data saved in the database to do the aggregation instead of like a waiting for the execution result. Okay, this is the uh main reason and in this case so you will not have thread runner or like other runner you are just have like one um uh like a function you only need to design one function okay for uh each processor for the execution so it will simplify the design okay actually yes so please take our advice.
Jude Pineda: Okay. Uh, yes.
Chun Shao: All right.
Zhanfan Yu: Yeah.
Chun Shao: Okay.
Zhanfan Yu: Try uh you explain more clearly. Yeah.
Chun Shao: Okay.
Jude Pineda: Yeah, I understand.
Chun Shao: Yeah. Okay. Now, yeah, we we we can have agreement and I Okay. I could say, yeah, now I'm more confident with this processor module and I think based on what we understand now, uh we can do it better. But now like good Jude, you pro uh like a uh like you you bring up this uh good question.


00:48:01

Chun Shao: What if delete? Now we need to think of it. All right, this deletion. Okay, you brings it up, not me. Okay, but it's good. Right.
Adrees Muhammad: Yeah. So, uh can uh like this three execution means we have three documents of one bank statement and uh it will uh each for each document we will have one execution. Is that correct?
Chun Shao: Um, yes.
Adrees Muhammad: And uh is it uh mean also like one document can have three execution. So
Chun Shao: Yeah, you made a good point. So, yeah, um, it's processor based. So, it could be different. All right. So in your like a data schema I'm also think about this like for this uh execution we may need to record another field called document ID. Okay so this u this execution okay for bank statement processor each document will be executed separately.
Adrees Muhammad: heat.
Chun Shao: So if they have uh three documents, there will be three executions and each execution uh aimed to one document.


00:49:22

Chun Shao: Okay. All right. Oh, you are fast.
Adrees Muhammad: Okay.
Chun Shao: You're already doing that. Okay. And uh but we do have other processor like uh for example driver license. driver's license will process the all the documents under one stipulation and with one execution. So let's say if we have like a two files, two images under this um uh driver license stipulation type okay and when we run the driver license processor there no matter how many files there there will only be one execution and the both image the driver license image the front and the back image will share um the same execution ID. Okay. So um so I'm thinking like which way is better to design either to put uh like the execution list here or like a in the execution you put a document ID but it will be a list. Okay. So that that means this uh or like you can put like a document ID. Yes. It could be a list. So this execution could involve multiple documents.


00:50:49

Chun Shao: It could not not be only one document. So this is for Javus license. And uh as we said before you can like force the processor to execute again like a rerun. Okay. And this will create a separate execution. All right. And if it rerun the processor um the previous execution will be marked as deleted because we only keep like a one uh execution there available for for for this uh document or for the processor. Yeah. So this will be handled by the processor itself. It need to determine like whether create separate executions for document or like a run a totally execution for all the documents and when a document deleted which execution will be marked as delete when there's a rerun okay which execution will be marked the previous execution will be marked as deleted so all all these kind of Um it's all detailed that is different from processor to processor uh that is need to be handled. Okay. Okay.
Adrees Muhammad: Okay.
Jude Pineda: So if I understand correctly, uh we have processors that either uh in documents.


00:52:29

Jude Pineda: Uh so we have processors that either run a single execution for uh in for a single document and there's also a processor that runs multiple document. Did I get that right?
Chun Shao: Yes. Yes. Like the driver license.
Jude Pineda: Okay.
Chun Shao: So no matter how many files they are, it could be two, it could be four, it could be six, depends on how many owners they have. So let's say in the beginning they have like uploaded two images which is only for owner one okay the driver license front and end front and back okay and later on they find out oh we have two owner and they require the photos of the driver license of the second owner and they uploaded two more files and while um even like In this uh popsup message, you only have the document ID of the two uh document that is uploaded uh like a newly uploaded document. But when you run the driver license processor, it will rerun and re-execute and process the whole four images. Okay. in this execution.


00:53:52

Chun Shao: So in the execution document ID it will be including four documents and the result will update the factors like it will create like a so the factor will be uh a list like for the for the for the owners okay for their credit score for example like a one is for the for I I don't know like a probably so uh But for the driver's license like a maybe the factor will not be credit score. It could be like uh the factor of like uh validation of the uh driver's license. So it's true or false the driver license is being validated. Okay. And you after you run it uh the factor will be updated. Uh previously it only like if it's a list it only have one validation and after you run again because they uploaded another two uh but they will not only add the two but they will rerun it and overwrite uh even though they are the same. The documents are the same. Okay. And the factors are the same but it will override it as both are true because the second execution gives out like a two factors for each like a like for these two owners.


00:55:21

Chun Shao: Okay. So you understand that?
Jude Pineda: Yeah.
Chun Shao: Yeah. Yeah. So basically like uh um for one processor we have many three different kind of processor. Uh one kind of processor it's only based on application form data. Okay. It's not any document related. It's just based on the form data. Okay. The second is document related but it will create ex each execution for each document. The third one is is document related but it will create a execution for all document under this distribution type. Okay, there's different three different kind of documents. And if you ask me like uh for the deletion, okay, for the third one like uh okay, they uploaded four, they have four photos, four images for driver license and they deleted two of them. Okay, they removed two of them. Then you will have another execution and this execution will only include the rest of one and you will update the factor. Now the factor list will be only one value there instead of two.


00:56:47

Chun Shao: The previous factor will have two values but this factor will only have one okay in the list. So this this is for the deletion. What will happen for a processor that process all the documents under one stipulation and we already discussed about the processors that will create execution for each document. How would we handle that deletion of the document? Okay. So now we haven't covered is what if the document uh the processor is not based on any document. It's based on the application form data for example the EIN number uh and we use the uh the clear report to run it. Okay. And what if they delete the EIN ID? What should we do? Okay. Okay. There is a obvious error that is the trigger is uh it's not a good example for for person is not EIN. If you scroll up a little bit scroll up a little bit. Yeah. For a person is not EIN. It's called SSN.
Jude Pineda: I'm All right.


00:58:08

Chun Shao: Yeah. No problem. Okay. So, what do we what we will do? like previously they have the information and then they delete it. It's not updated. It's not like they create like they update the yin number. There's a typo. Uh so they Okay.
Jude Pineda: So if they delete if they delete the AI engine, I think uh I think it's the part of the API module to run some validation checks for that.
Chun Shao: So like it will still be included in the update pops message even though it's delete one one field in the application but it's still in the update pops message uh but the difference is uh like in the pops
Jude Pineda: Oh, okay.
Chun Shao: message it will include okay I updated yeah in the new value is none there's no new value Okay. So if they have a value, what you will do is simple uh run it again. Okay. Another execution based on this one. But what if the new value is null? What you will do?


00:59:19

Jude Pineda: I think it will just execute and it will just throw a validation error for the processor since uh the AI in is empty.
Chun Shao: Uh okay. Can you say that again?
Jude Pineda: Oh, I'm sorry. So, uh I was thinking of putting some triggers here. So, I think it should also be validated here. Yeah, I I take back what I said earlier.
Chun Shao: should also be validated.
Jude Pineda: So, so so if if they if they uh updated uh the SSN or EIN to an empty so I think it will not execute because it's empty.
Chun Shao: Uh okay.
Jude Pineda: There's nothing to process.
Chun Shao: So what about the previous execution?
Jude Pineda: So uh for that uh yeah uh yes I
Chun Shao: So the previous exusion should be marked as deleted soft delete right.
Adrees Muhammad: I guess we can generalize this concept like if we have a new uh updated value we just uh mark the previous one as outdated or deleted. So can be generalized.
Chun Shao: Mhm. Yeah. Yeah. And because the new value is empty is now.


01:00:43

Chun Shao: So there will be no new execution.
Adrees Muhammad: Yeah.
Chun Shao: Yeah. Yeah.
Jude Pineda: So, so uh it's uh is it going to be handled by the API or in the processor?
Chun Shao: So that's good. No, it's like a it's it's it's actually it's no uh no change. Okay, it's just like the when you write the program when you handle this situation you just remember if there is any update and for this processor if there is any uh previous execution uh which is not marked as deleted you should delete it. So for each processor you should only keep one uh available uh execution or zero zero available execution or one available execution. You should not have like more than one execution uh like for this processor unless it's like a it's multiple it's document based okay for each document. So for three different types of processor, the first and the third processor, you will only keep one. Okay. Only one. That's it. Oh, okay. Yeah. Okay.


01:02:03

Adrees Muhammad: June we need to uh like uh change the status of factors pre-check and other calculations as well in that case not just a processor execution I guess so that like EIN we we have EIN so we will create
Chun Shao: Okay. We need to
Adrees Muhammad: factor against it as well so another uh like logic is the pre pre-check and the scorecard and uh so we need to update everything in the case of uh uh it's uh a new value.
Chun Shao: Uh um yeah, we actually um for secure for this factor part they don't need to change anything it's just like when
Adrees Muhammad: So we need to mark the previous value of each entities as uh outdated. What do you think?
Chun Shao: we mark this uh like uh as invalid or out ofdated or soft deleted whatever you call it we should update the factor also okay even if there is no new execution we still need to do the aggregation based on the current data Okay, this is also yeah for the processor part once the processor part yeah has been uh done like it will update the factors uh no no other module will change


01:03:16

Adrees Muhammad: So it will uh skip the processor part and will do the rest in that case.
Chun Shao: anything it's just the processor part so this is also one good part for like the aggregation is independent to execution so if there is no execution like this this There is no new execution. The first step is you receive the request. Okay, I need to create execution. Then the second is I mark the current active execution as out of date or delete it. Okay. And the third step is to run a new execution or not or not run. Okay. I like like in this case if it's delete then will not run. And the fourth step whether you run or not run I will always execute is this aggregation based on the current data. So if I let's still go back to this yen and clear report. So uh because we uh mark this uh uh this execution as disabled. So there will be no data. All right. And uh all the factors we generated previously like uh the um that said the factors are related with this uh uh with this clear business report will be all marked as missing data.


01:04:59

Chun Shao: So there will be no data or will also be like removed. Okay. Um oh it's not removed like so for the factors how we like a market as this value is yeah probably will have another value as now okay create a new like this is now value and uh
Jude Pineda: What was that? I did.
Adrees Muhammad: status. Introduce a new status.
Chun Shao: is it uh better to market as uh let's Think about it. So what if they have a new assession later once we delete it and they give another new EIN number. So there will be a new execution and a new aggregation and this aggregation will try to find the most upto-date uh factor and create a new one and uh link this the previous to the new one. So it it doesn't matter. Okay. So it will it will not matter either you set it value as now or like you mark it as uh uh deleted. I I I prefer like uh uh you can mark the value as now.


01:06:21

Chun Shao: Okay. Talk this with Sahil because this will relate to Sahil like what he expected for the factors. Mhm.
Adrees Muhammad: Like if we have a new factor then we can link it with the previous one but in case of deletion or in that case we will not have a new factor and the current one will be let's say maybe outdated order it's not relevant now. So we need to add in that part. Maybe we can introduce a new status or
Chun Shao: Okay. Yeah, probably we can introduce like a um yeah maybe just a boolean indicator whether this factor is uh is available or not like it's uh I I don't know maybe you can find a better name status could be uh yeah status usually like you should have uh three or more different status if you only have like two status it's just like indicator Whether this is uh valid or
Zhanfan Yu: Um so what does the mean uh link means that uh address you said that whenever there's the way that we link with previous value or previous vector


01:07:40

Chun Shao: Yeah. Yeah. The the last one. Uh, sorry. This is not Oh. Oh, wow. We are We're late for the next meeting. Sorry. I I I I should speak to Ali.
Adrees Muhammad: Okay. So basically uh we have a property supersedes ID in factor. Uh so it reference to the factor. It's previous version of this factor. So we can say that we are uh here we are managing a history of the factors. So that what I mean
Chun Shao: Yeah. And previously uh designed here is like a super seed ID. So like the first factor the superity will be now the second factor if there's new factor it will be the superiz will be linked to the previous factor. Okay but my suggestion is like a instead of using superers size it's like a uh it could be like a renewed ID or like a uh replaced ID. So if any factor with a renew or replace ID that means this factor is uh not valid anymore and you need to find this renew or uh renew ID as now then this is the most up to date otherwise let's say okay in extreme case if there is a factor has been renewed 100 times how to find the most up to date you need to first find the ID that is now this is the first then


01:09:17

Chun Shao: uh you run 100 times to find about who is the last one most up to date one. Okay. So this is not very efficient.
Adrees Muhammad: So I will check it.
Chun Shao: Yeah.
Gene Rellanos: I have a question for the factors. So in the super since I did so we so uh we only care for the latest uh factor data right we don't need to really care for the sequence we just need the latest data.
Chun Shao: Yeah. Yeah. They don't care about the history. They only care about the latest data.
Gene Rellanos: Okay. So, we don't really care if the maybe the sequence is break broken for the for the soap seeds. So, Okay. Yeah, I understand.
Chun Shao: Okay. Yeah. actually uh like what Andre is told me is like so he will create a like a snapshot of the factor uh generate a hash code let's say okay for example um um if the like let's say we have a factor called uh average monthly uh revenue okay and uh with the first two bank statements we get a result as uh 10k okay and the third bank statements happen to be 10K.


01:10:48

Chun Shao: So the factor will be renewed but the value will remain the same.
Gene Rellanos: Mhm.
Chun Shao: Okay, 10K then the hash code will not change. Okay, the hash code will not change even though there are new factor but the value are the same. So because the hash code don't change, they will not do the re-evaluation. Okay, so that can save some time. So yeah, so this is this is a good part that we designed this like a modules like only responsible for itself and uh so this factors is like a bridge between the processor and the pre-check and the business
Gene Rellanos: Yeah.
Chun Shao: score everything but because it's like a uh it's it's like a separately. So we can what we can do is we just focus on each module to do its job its own job correctly and then the whole system will run smoothly. Okay.
Gene Rellanos: Okay.
Chun Shao: All right. Yeah. Um so uh Jude let's come back on Friday. Okay.
Jude Pineda: Okay, sure.
Chun Shao: Yeah.


01:11:59

Chun Shao: Please put those like a delete and also like another uh uh popsup message you should listen from the API is this uh execution like a force execution uh of one processor. Okay, let's discuss on Friday.
Jude Pineda: What happened?
Chun Shao: Yeah,
Adrees Muhammad: So I have uh like couple of questions. First of all uh what are different entities we can delete? Like we discussed we can delete documents but uh there are other entities as well. So we need to uh work on those as well. So what will be the scenario? So what are the other entities we can delete as well?
Chun Shao: Okay. Like underrite. Yeah. Yeah. We can discuss it. Like underwriting uh document uh they can all be deleted. Factors they can deleted. Okay. Business rules um like a suggestions almost everything can be deleted.
Adrees Muhammad: Okay. And uh the next question is uh let's say a user delete a factor. So what it effects on uh processor bar?


01:13:15

Chun Shao: No effect.
Adrees Muhammad: So like uh it's not in display um like shouldn't affect anything.
Chun Shao: No, no. Um, if they delete a factor, okay, Z will only be like marked. Yeah, this is good part like if you introduce a status. So, the status of this factor will be marked as deleted and it will not be considered in the how to say in the in the in the pre-check criteria business rules. Okay. uh but if there is a process execution and the result is updated this proc uh this factor so the previously deleted and uh it will be updated as like I have a like a renewed uh ID okay and this ID will indicate to a new factor and this factor status is not deleted so they will see this factor come back again all Hi.
Adrees Muhammad: So like like uh from the user perspective let's say on front end uh user delete a factor so uh it's showing that he has run the processor which results to that factor so he want to to like this factor to to be display again so after deletion it will not no longer be displayed on front end so he want to display it again so what he should need to do he should need to run the processor again or


01:14:54

Chun Shao: No, he there there should be a there should be a toggle button that they can switch on and off to show or uh like a deleted factors. Okay. So by default this deleted factor will not be show in the list but they can toggle on to show all deleted factors and they can check the history of this factor the change of the value.
Adrees Muhammad: Okay. All right.
Chun Shao: Okay at what what date what time uh with which execution uh it gives you this result. Okay. At what day what time for which execution it gives you this result. Okay. and like uh okay for example okay at today okay uh October 1st uh 11:15 by the bank statement processor okay this uh monthly average revenue is like a 10k okay then it was deleted uh okay uh like by what time okay with uh which processor okay uh with uh no there is no execution but it's deleted Okay. And then it's updated again uh by the bank statement processor because there is a new document uploaded.


01:16:14

Chun Shao: So it can view the history. And for the deleted factors uh it's in the database. It's just uh we can toggle on and off to show them or not.
Adrees Muhammad: So like what I thought like uh it's in the deletion stage. Okay. So as you said if he want to update it he need to re-upload the document and if he reupload the document then the processor will run again and uh if it's the same document then it will be like a redundant part. So is he can move the like factor from deletion to enable state instead of just re-uploading the document for convenient part because uh it
Chun Shao: Mhm. Um yeah. Yeah. Probably we would allow them to like enable this factor like from delete to like undded. Okay. So like uh like I said um the factor could be like from a execution or could be like just manually created or updated. So if you from here that like you have a execution right this factors you have uh do you save a like which execution ID it comes from?


01:17:35

Chun Shao: No like uh the factor have ten ID.
Adrees Muhammad: Yeah, you infected.
Chun Shao: Oh yeah yeah yeah and you also have like a created by Okay.
Adrees Muhammad: We have execution.
Chun Shao: And uh probably yeah you can also have a updated by. So this will record this uh uh account ID or user ID who updated manually. So this will indicate okay this factor is updated by a execution or by a person.
Adrees Muhammad: Okay.
Chun Shao: Or maybe not updated. Yeah. Yeah. Updated by like it's been changed. So yeah, it's not created by it but could be updated by a person.
Adrees Muhammad: So in short we want to allow user to do anything uh any kind of updation in any entity like any kind of updation in any kind of entity like in factors he can update those
Chun Shao: Okay. is that again allow user to do any what uh it's very hard to answer this question because we have lot of entities we I cannot answer this unless we go through this uh
Adrees Muhammad: check he can update Yeah, you got that.


01:19:03

Chun Shao: schema again yeah okay so yeah that means We need to make a appointment with other schemas.
Adrees Muhammad: s***.
Zhanfan Yu: Um, what about we have a meeting tomorrow uh for the processor and then uh and then we uh I mean like without having the delay logic but just like modify the current and then uh because I feel like
Adrees Muhammad: Okay.
Chun Shao: Okay.
Zhanfan Yu: the deation logic will be uh the system So we need to think it carefully and more thoroughly.
Chun Shao: Okay. Yeah. Like J you are you available to have all the documents ready by tomorrow?
Jude Pineda: uh what documentation? Oh, okay.
Chun Shao: Yeah.
Jude Pineda: I'm sorry.
Chun Shao: Update.
Jude Pineda: But I I just have one more question actually uh Jeremy engine mentioned. So back to uh uh individual execution of the processors for let's say back to back bank statements. uh since we're going to execute it in in a parallel sense I think there's going to be a problem with race conditions like what if both documents happen uh around at the same time so they both uh they both have previous uh extracted the previous historical data uh but during the update so it's going to be incorrect because one is not referencing the the part uh the the other execution


01:20:41

Chun Shao: Yeah. So um like to solve the conflict of this parallel things maybe my suggestion is that uh we may need to add a indicator in the database. So when there is one execution doing this uh aggregation job other other like uh other aggregation well wait there until like this indicator has been turned to like off. So yeah this can solve some like a conflict in the parallel processing problem. Okay if it's necessary I mean if it's if it's could be a problem.
Zhanfan Yu: Wait, what's the question?
Chun Shao: Yeah.
Zhanfan Yu: I do not understand it clearly.
Jude Pineda: uh so uh Jeremy let's say uh we have March and April bank statement so if uh if we process it parallel uh so and finish it around at the same time so they're going to have to uh based on based the factor of the previous result, right? But since they both are finished around at the same time, so for the month of April, it's not going to have the data from the March uh bank statement. So, I think there's going to be an issue uh for that part.


01:21:58

Zhanfan Yu: Wait, you said that uh the the March and April finish at the same time.
Jude Pineda: Yeah.
Zhanfan Yu: Then what will cause the issue?
Jude Pineda: Yeah. So since uh since the Mar since let's say April needs the data from March or March needs the data from April then yeah there's going to be an issue for the factors that's that we need to aggregate.
Zhanfan Yu: Wait, what? Why March need data from April or April need? What what data specifically that will be needed?
Jude Pineda: Uh so yeah back to our example as uh earlier. So let's say the a average uh non-sufficient fund days uh is it days or average uh daily balance I'm sorry I forgot factors so yeah we
Zhanfan Yu: Yeah, that the a average um I mean like the March will have its own average and April will have its own average and then it will both aggregate to the database.
Chun Shao: Yeah, if there is no data then there's no data it will be handled like you only upload April. If the March is not ready and uh it it will be like a they upload it April 1 then after one day they upload March and after another day they upload May separately.


01:23:29

Chun Shao: So what are you going to handle this situation? Right.
Jude Pineda: Uh yes.
Chun Shao: Yeah.
Zhanfan Yu: Yeah, I mean the only problem that I can think about is that um like you need a lock for the database inconsistency because like when you read the value from the database and And meanwhile the uh the march write the data into the database. Uh so you may read the wrong data or outdate data. So that that might be the issue that I can think about and you need to use a lock for that but otherwise I don't think there any problem with it.
Adrees Muhammad: Okay. So I can answer that part. So in the database we will handle that part like uh the read or write operation we will set the priority of the post like uh if a user want to write or read something at the same time. So we will set the priority. So we will do the read operation first and then we will do the right operation In the first. we have currency control concept here.


01:24:47

Adrees Muhammad: So so that the database is consistent and have the transactions. So if one operation fails in the transaction all the transaction is fail. So we will have a consistency. Yeah.
Chun Shao: Okay. So I I will I will give you example like extreme case. Okay. So let's say we have two uh bank statements and both processed and both enter the aggregation stage. All right. And uh okay now now this this could be a problem like a so for example the March has been finished and write the data to the database and the next one is it will run the aggregation and then the computer switch to April because they receive the April data and they also want to write to the database. So it will run April right to the database before the execution of aggregation of March and uh unfortunately after the April write to the database the computer choose to continue run the thread of April and do the aggregation before the March. Okay. So then the April aggregation will find out okay we have two months data in the database and I will generate a factor which include two months data and after that finish it switch back to the previous March thread to do the aggregation but that aggregation data only contains itself.


01:26:32

Chun Shao: So it will also generate a factor but this factor actually only contains one month data and because it's generated after the April's factor so it will become the most up-to-date factor. Okay. Now we will have a problem that is this aggregation is only based on one month data not two months. This is one problem I could think of.
Jude Pineda: Uh so uh what about uh what if we just uh skip the parallel processing if that's the case for bank statement? Let's say let's just say if there's six uh what if we just uh process it uh sequentially. So there's no need for I'm sorry.
Zhanfan Yu: I mean I mean even though that you you skip the bank statement you also have other statement and you will face the same problem like you you have other documents but some factors are shared between the documents.
Chun Shao: Yeah, if yeah I mean if it's among different like uh processors like one factor is shared by two processors so we have no choice it's just the first com first so
Zhanfan Yu: So I mean this is a problem that you need to solve for the par when when you are choose to use apparel.


01:28:12

Chun Shao: the second com will override the previous one that is no problem but uh if we I could talk about the multiple execution and the overwrite of this uh aggregation and this is obvoid here.
Jude Pineda: Yes. But uh what but if we use this uh flowchune I think that's not going to be a problem.
Chun Shao: Yes, I said you free this up.
Jude Pineda: Yes, Jun. I was actually concerned uh for the race condition, June, if we uh yeah, if we what if the both uh multiprocesses uh finish around at the same time. So, it's going to pull a data is it's going to pull a empty data. It's going to be uh uh just created. So, yeah, because this one uh all of the results are going to be aggregated uh in a single way. We don't have to aggregate uh every execution.
Zhanfan Yu: Yes. So this is execution for the bank statement. I mean you can avoid the the uh risk condition for the bank statement but in parallel you have another execution for another processor.


01:29:31

Zhanfan Yu: So that's why I suggest that I mean not having like two level par parallel. So your design is that uh let's say that we have a bank statement processor and then inside bank statement processor you do a parallel and then do the aggregation but outside the bank statement processor you have another processor executed in parallel and which might have another parallel so that you have two level of par parallelism
Jude Pineda: Uh yes that's what uh what what I'm designing uh journey uh just that uh from my understanding of what you want me to make is that individual bank statements for let's say month April May June July so those three bank statements it's going to be handled uh different uh in a different processor execution not in a single execution
Chun Shao: Okay.
Zhanfan Yu: Yeah, but like your your design diagram is not clearly identify that.
Chun Shao: We Okay. Uh I have a suggestion. Okay. We can we can both. Okay. First we can accept like one level of parism from Jeremy. The second we can do this aggregation after all the process has been done.


01:30:49

Chun Shao: Okay. So it will be like this. Um when the processor received the popsup message it will determine okay how many processes will be there and for example it says find out three processes and five executions will be generated. So five threads will be generated but this aggregation part for this processor will not be uh like executed unless like uh all the processor like all the executions has been done. So this aggregation operation will be performed after the execution. So you separate this execution and aggregation. Is that okay?
Jude Pineda: Oh yeah.
Zhanfan Yu: Yeah.
Jude Pineda: Okay. So yeah for for the aggregation part. So is it going to be a new processor or Okay, got it.
Chun Shao: No like a aggregation. Okay. So for each processor we need to provide two functions. One is execution, one is aggregation. Okay. Yeah. So execution is running. Okay. You take the input, you pre-check everything and you like either core API or like you do some calculation inside and you have a output result.


01:32:19

Chun Shao: This output result is not factor. It's the processor outputs. Okay. You save somewhere. All right. And then Yeah.
Jude Pineda: So it it's going to be a new Well,
Chun Shao: Yeah. Like a in in this table processor execution you could design like a uh like a output which it could be a JSON formatted uh data something like that. Okay. You talk with uh address C where you put this. Okay. Then there will be another one uh what we call okay let me explain further more so this output could be like for bank statements it's a JSON formatted result returned from uh the bank statements okay and for JS license it could be this like uh okay for for the like a clear report it could be a huge like XML format reported report you received and also you need to receive a uh PDF file saving the data link and point a link to it that they can download the report. Okay, this is like a this data uh output you get but it's not factors.


01:33:30

Chun Shao: So uh in the aggregation function for each processor it will actually it's independent from execution. So it will actually go to the database find out all the available uh output and aggregate and generate those factors update those factors. Okay. So this is most updated. So this will also handle the deletion situation. So if you delete one document or one execution and the output like will be marked as deleted. Okay. And the aggregation will renew uh the factors based on like okay previously I have this output but this output would not be considered in this uh aggregation anymore. So the factors will be updated. Okay. So in this case we can solve the problem.
Jude Pineda: Oh, okay.
Chun Shao: Okay.
Jude Pineda: Yeah, I'm here with that notion.
Chun Shao: All right. I think it's a good discussion. We we are more clear and uh we can finally have some agreement.
Adrees Muhammad: like I regarding aggregation uh I have a suggestion maybe I'm wrong like uh if the executions are linked so we can generalize it in that way if the executions are linked then on each execution we can run the


01:34:52

Chun Shao: Okay.
Adrees Muhammad: uh aggregation like let's say if the we have a in a parall case we will run one aggregation that's fine if the document let's say 3 months document it will be if it's divided ed into two parts. First user uh give two months document then later on one month's document. So still these are connected. So these are connected. So we can run the aggregation in the second uh part as as well like in the case of uh processing one uh month statement. So that will be generalized in that way. If the executions are linked, we can run the aggregation after that. uh it uh will become independent to the user if we can uh upload the two month statements at once or three month statements at once or uh after an interval.
Chun Shao: Yeah, it can be implemented in the aggregation like for example it will not do the aggregation unless they collect at least the three months bank statements then they will do the aggregation right. Yeah we can we can define that and the user can like a uh they can set it up like some user they require for three months bank statement some they require for six months bank statements.


01:36:20

Adrees Muhammad: Yeah.
Chun Shao: Okay. So for this like a processor we can have like a parameter uh when they purchase the processor they can set it up.
Adrees Muhammad: s***.
Chun Shao: Okay. And the bank is is the only one that that I can think of. Okay. The aggregation will be act will be performed only certain condition has been satisfied.
Zhanfan Yu: Um, what about this? Like when we uh encounter the uh enter the processor module, we first uh determine what are the processor need to be run and then we parallel run all the processors with all the documents and then we got the result like uh the output from each processor uh parallel execution that output one two three and four like we have five output So one to five and then we do the aggregation on all the output result like now we have output one to five and then we do the aggregation to aggregate from the output one to output five to update the all the factors related to
Chun Shao: Okay, the problem is the aggregation is independent to execution.


01:37:57

Chun Shao: So it's not rely on the execution result solely. It will rely on all the historic data may not all uh listed in this executions maybe in executions.
Zhanfan Yu: Yeah, I mean yeah so that's why uh I mean but the historical data is only related to this underwriting application, right?
Chun Shao: Yeah. Yes.
Zhanfan Yu: Yeah. So, like we aggregate from output one to output five like it can still see the historical data, right? Like uh for example the uh with uh we uh all the factors at the beginning are zero and then we aggregate output one to all the fac to update all the related factors and then we aggregate the output two and then update all the related factors like uh the output two now can see the uh the historical data of output Right. If you need some like average,
Chun Shao: Yeah. Yeah. But since like we already wait for the completion of all the executions like the like we we don't need to do like perform three separate aggregation. We just need to perform one aggregation.


01:39:27

Chun Shao: Right?
Zhanfan Yu: say it again.
Chun Shao: So let's say okay we have three processor and five executions uh that's because one processor is bank statement process and has three executions and we have five outputs results okay and uh so we uh we instead of run
Zhanfan Yu: Yeah. Yeah. Yeah.
Chun Shao: five aggregations like a two for the other two processes we don't care but for the bankston process we only need to run aggregation once That's it. We don't need to run three times aggregation because all these three aggregation has already been uh output and the result saving in the database. So we need to only run once for the aggregation for bank statements. That is enough.
Zhanfan Yu: Okay.
Chun Shao: Yeah. So the aggregation will not take any input. It's just perform it aggregate and the data will be from database.
Zhanfan Yu: Oh, but what about like uh like now we have bank statement processor and we have another processor. Uh there are some factors interact or overlap.
Chun Shao: Yeah.
Zhanfan Yu: How we going to do the aggregation for that?


01:40:42

Chun Shao: Okay. So, uh it will be separate aggregation and will be performed sequentially. Uh and in this case we can determine the priority of which processor.
Zhanfan Yu: Yeah. So the problem is that how we do the like ensure that we process it like uh like the because for this case that we still have the data raising pro condition or problem
Chun Shao: What did the racing condition problem?
Zhanfan Yu: because for parallel that we run the bank statement and another processor at the same time right so we don't know which one will finish first and then they might finish at the same time.
Chun Shao: Uh oh. Okay. So it doesn't matter.
Zhanfan Yu: So that it will create the data.
Chun Shao: It doesn't matter because the aggregation will only perform after all the execution finished. No matter how many like a five or six it will wait until all the execution finished.
Zhanfan Yu: Yeah. But but you said that u the bank salmon will have its own aggregation.
Chun Shao: Yeah, each processor will have its own aggregation.


01:42:04

Chun Shao: Okay, let's say this. Okay, um I give you example for the credit score. Okay. So, credit score could have this factor could have two sources. One is from application form.
Zhanfan Yu: Yeah.
Chun Shao: Okay. Directly they write a credit score and the other one is from credit score report.
Zhanfan Yu: Yeah.
Chun Shao: Okay. So, when they purchase processor and they can set up the order of the processor. Okay. address we need to add one more thing is when they purchase a processor for uh like a one tenant uh there is a index for this processor okay so based on this index they will run the aggregation now I will explain what will happen so for the application processor the execution what will almost do nothing it's just like we forward the data okay that's it okay and then uh We record the data. Okay. But there is another processor which is a credit uh score report. It will run and uh uh the whole thing will not run the aggregation until this uh credit report API returns a result and the execution finish.


01:43:18

Chun Shao: Now let's say the the application says their credit score is 700 very high but the credit score says you only got uh 650. So when we do the aggregation we can set up the aggregation sequence based on the index. So usually they set up the less uh like a reliable source as higher like a lower uh like a not not lower like a the less the smaller index. So it will run the aggregation first for the application processor. So it will say 700 and then because we uploaded uh like a run this credit report and it will override it with 650. Okay.
Zhanfan Yu: Yeah, I I can get c get your idea here.
Chun Shao: Yeah.
Zhanfan Yu: But uh what about like uh like theoretically um like we have uh three credit score document. So, so like one uh one application form but three credit score documents and then are you going to do the uh like uh within the credit score uh processor you're going to do the aggregation first or you're going to I mean h how you aggregate three credit score documents like this is like compared to like a similar scenario with the bank statement


01:44:52

Chun Shao: So for like a a credit score processor uh when you talk about this document actually there is there will be no document related for this processor. So when you talk about this document is is it a result like output result they get from uh API
Zhanfan Yu: Yeah. I mean, let's let's just assume that like uh like because if you have three bank statement, you're going to have like three result, right? You're going to have three three execution running in the parallel.
Chun Shao: Yeah. Yeah.
Zhanfan Yu: But let's just assume that we have three um credit score execution running in the parallel. How you going to handle the result? Because now that the factor credit score are uh effect uh I mean need to be uh changed or affect by both application and three credit score. are gonna handle this case because this is the case that um Yeah.
Chun Shao: Okay, first uh well it will not happen for credit score because the credit score will only run once and return one document unless like you like uh forcely to execute another run like you want to recheck for example like you check the credit score one week ago and applicant requires you to run another credit score because he like he believed his credit score raised up a lot uh in this week.


01:46:27

Chun Shao: So you run again and when you run again um there is a new uh execution will mark the previous execution as uh deleted and you only have one uh report document to uh to aggregate the picture.
Zhanfan Yu: Yeah, but I I I just want to use this as a like uh hypo hypothetical uh example that like for example that uh we are processing a bank statement but bank statement affect uh will uh the factor related
Chun Shao: Yeah. Yeah. Yeah.
Zhanfan Yu: to bank statement also affect by another um like processor like probably the application processor. Yeah, because we said that we're going to uh run the three bank simmon execution in parallel and then aggregate the bank simmon result and then we want to and then I mean this factor will also be affected by
Chun Shao: Mhm.
Zhanfan Yu: another processor. How we going to handle this case?
Chun Shao: Yeah, as I said, uh we we can handle this by the sequence of executing the aggregation. Okay. Actually, there is one good example like uh in the application form they are allowed to uh provide their monthly revenue.


01:47:46

Chun Shao: Okay. So they can fill in their monthly revenue. How much is it? And they feel a high number. They said okay I have 20k and uh because the aggregation like is first first aggregate the application form then the factor will be 20k but after execute the bank statements uh uh aggregation it becomes 15k. So this 15k will override the 20k.
Zhanfan Yu: Yeah. Uh I think that that is uh like uh we have the same idea as I previously proposed.
Chun Shao: Yeah.
Zhanfan Yu: we will uh run the all the execution in parallel and then get all the output but you just give it index so that we aggregate the output in a certain order right
Chun Shao: Uhhuh. Yeah. Yeah. Uh not okay. aggregate each processor uh in a certain order not output output is finished. Okay, the aggregation is has no not known it's not related to the output of the executions this time.
Zhanfan Yu: Well, uh I like
Chun Shao: Aggregation is very independent. Even there's no excusion, there could be aggregation.


01:49:18

Chun Shao: Can you understand? Even there's no execution, there could also be exec aggregation. For example, they mark it as deleted. So there will be no new execution, but we need to rerun the aggregation to update the factor.
Zhanfan Yu: Um but like to me the even though the there's new I mean there delay factor there is no uh I mean there there's still a like execution but the just the execution will not take any effect or actions because like when when you update a uh when when you receive a delayed update and then the execution will be you deleted uh and then you update all the related
Chun Shao: Uh, what do you mean not take effect? So, Yeah, I think what uh
Zhanfan Yu: vectors to none, right? And then you do the aggregation.
Chun Shao: what we talk with address we will not uh market as now we will like change the status as deleted. Yeah. But similarly yes.
Zhanfan Yu: Yeah. But there there's still some like sort of execution on there.
Chun Shao: Yeah.


01:50:45

Chun Shao: Sort of execution. Yes. Deletion of execution. Excuse me. Yeah. So, what is what is your question? What is a puzzle part of this?
Zhanfan Yu: Um, Um yeah. So I will sing more. Uh I think I will sing more and then I will see the the design tomorrow.
Chun Shao: Okay, what what do
Adrees Muhammad: So uh how can we define how many executions we need before we need to do the aggregation? Should uh will we add that part in any table or uh where we will define that part.
Chun Shao: Um okay basically um it's depends on the processor and the only thing I can sort of off is only bank statements. Okay they require usually industry standard is three months bank statements but some MSA company they might require half year bank statement. Okay. It's it's no harm if you do like if they require six monthly spec statements. It's no harm to do aggregation if you only collected four of them. Okay.


01:52:45

Chun Shao: Uh but we can set it up. Okay. uh like it will not do aggregation unless we have like uh five uh like uh executions or outputs or six executions of outputs available uh there. So yeah and uh okay this can save first this can save some uh energy uh like a running power. Uh the second is um alo okay it could be used that we do not need to create another factor that we will only pass this factor once we get uh six uh mousees uh bank statements. Oh, okay. So, we can save one factor there. Um, yeah, this is what I thought.
Adrees Muhammad: Where will we save that part? Like uh uh we will define that thing uh we need to uh like run the uh for the bank statement we if there will be four execution then we will run the aggregation. So these are uh rules. So we need to add those as well because in future let's say another for another stipulation we will have aggregations as well.


01:54:09

Adrees Muhammad: So we need to uh discuss the way to store that part as well. So that uh it should be generic and uh yeah for the whole structure because when we run the aggregation it will uh it will use that structure to run the aggregation uh as a trigger. So uh that's why it will be a generic protocol.
Chun Shao: This will be trigger. Okay. Okay. This can be solved like a triggered inside the aggregation function. inside the aggregation function. We can handle this inside the aggregation function. So it will not affect other processor if it's different like they don't require any uh like a criteria to run this aggregation as long as like there is one. So by default there's must be like a one execution or maybe no executions also. So there is no criteria but uh the only like a criteria is for the bank statement is different. It will only run when you have a certain available uh outputs there executions there then you will run it. Okay.


01:55:37

Chun Shao: Otherwise you will mark all the current factor related to it as disabled or less invalid. Okay, if there is any. So this this can be like different inside the aggregation. So we we only care about now for now we only care about the whole like as you said the interface the basic uh interface of all these functions but like the difference the unique uh for the bank statement we can handle it inside the aggregation function. Yeah, but when we when we like write the documents regarding what should we do in aggregation, we can write a like a general uh instructions of how to write this aggregation. Uh and uh one part could be like uh for uh bank statement uh processor when you write the aggregation function you need to check okay how many uh executions available executions not deleted are there which is required to perform this uh uh aggregation.
Adrees Muhammad: So it means like after each uh execution we will check how many execution we need to perform the aggregation. So as soon as we so like uh


01:57:10

Chun Shao: No, no, not after execute. The check of this is in the aggregation. It's not at the end of execution.
Zhanfan Yu: Uh I sorry for interrupt I have another meeting with the bank statement. So uh let me
Chun Shao: Yeah, me too. Um, so I'm so sorry for Alli. Uh, okay. Are you available at three, Jeremy?
Zhanfan Yu: check. Um, probably not cuz uh today I have uh I need a today is a Wednesday. I need to meet with the bank statement uh and help them solve the problem for the Friday demo.
Chun Shao: Okay. All right. Uh so let's do this. Okay. Uh let's try to meet with Ali tomorrow morning 10:00 a.m. Okay. And uh then after that we can do with aura processor. Continue. Okay. At 10:30. How's that?
Zhanfan Yu: Yeah, it works. Um, shoot.
Chun Shao: Okay.
Zhanfan Yu: Uh, can you also uh for meeting tomorrow? I want to see the like one high level design and because now that you have the uh detailed uh diagram for the workflow but I want also have want to see the high level um design that how how we parallel the processors.
Jude Pineda: Oh, okay. Sorry, I muted. Okay, got it. Uh,
Zhanfan Yu: Yep.
Chun Shao: Okay. Let's meet uh 10:30 tomorrow. Okay. All right.


Transcription ended after 02:00:09

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
