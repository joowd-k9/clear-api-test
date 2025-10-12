Oct 2, 2025
AURA Processor Design - Transcript
00:00:00

Gene Rellanos: Good morning, Jude.
Jude Pineda: Good morning, Jane.
Chun Shao: Sorry. Sorry. I was uh we were on another meeting. Okay. Hi, Jude. Jenny.
Jude Pineda: Oh, hi John.
Chun Shao: Yeah.
Gene Rellanos: Hello.
Chun Shao: Yeah.
Gene Rellanos: Good morning.
Chun Shao: Sorry. Uh we we were on another meeting.
Gene Rellanos: No worries.
Chun Shao: Okay. Yeah. And this is the debt you need to pay because yesterday we spend a lot of time and cancel that meeting. So today I put it put the other meeting earlier than you. So all right. Okay. So let's let's go over this uh notion document again.
Jude Pineda: Uh, will I be the one sharing or you? So uh this is for the orchestration part. Uh I have added uh another topic for the manual execution where we uh put the underwriting ID and which processors to execute.
Chun Shao: Mhm.
Jude Pineda: And then we uh pass the documents list and the stipulation uh and the ids of the that stipulation.


00:12:57

Jude Pineda: So yes, this is the this I'm I'm sorry.
Chun Shao: Oh, you're too fast. Sorry. I I'm just finished looking at the first uh pops of message. Uh can I scroll up? Yeah. Okay. The second is updated. All right.
Jude Pineda: Yes.
Chun Shao: Uh yeah.
Jude Pineda: for the updated one.
Chun Shao: Okay.
Jude Pineda: Uh this is where also the the documentation will be uh triggered.
Chun Shao: Mhm. Okay. Yeah. Okay. Uh yeah. Good. Good. Good design. Yeah. This this is much better than what I designed. And uh do you have a contact SD? Make sure she knows what kind of message she should uh emit.
Jude Pineda: Uh yeah. Well, probably should.
Chun Shao: Okay. Yeah. Yeah. This is this is really good. Okay. Uh you have uh Okay. Yeah. Um updated, created, deleted. Okay. Good.


00:13:56

Chun Shao: Next.
Zhanfan Yu: Oh, wait.
Jude Pineda: So this is the Okay.
Zhanfan Yu: Oh, go back a little bit. Yeah, let me check. Okay.
Chun Shao: Oh, for the owners like owner owners score one. You think the is this a good way to to put it there or like uh do have other better ways to do that?
Jude Pineda: I think it's a better way because uh let's put it right that so yeah because I want to use this uh wild card so it's easier to for me to match it so in filtration part in this Wait wait wait can I go here first J for the uh for the uh arch I mean high level overview first so yeah these are the pub subtopics so and then if that
Chun Shao: Mhm.
Jude Pineda: if there's a publish data so we the orchestrator orchestrator we're going to receive that message and then we'll normalize the payload and then we'll select the processors. Now, so before we have we can select processor the processors we have to resolve it first from the registry and then we're going to map it to the actual classes and then add for select processors.


00:15:30

Jude Pineda: This also means the filter filtering uh of the processors based on triggers. So uh yeah and then we execute those filtered processors and then the aggregation and uh storage to database. Yeah.
Zhanfan Yu: Uh wait, did you check my uh new orchestration design or use the old one?
Jude Pineda: So, I'm sorry, J. I didn't what
Zhanfan Yu: Uh I mean is this design based on the old uh orchestration design or the new orchestration design?
Jude Pineda: all the the previous file. So, yeah, I just modified uh a bit in the in this I mean I just made this more simpler actually the high level design this is actually based on the previous one but for the what's happening inside this uh inside this part is uh updated.
Zhanfan Yu: Okay.
Jude Pineda: Okay. Then for the filter part uh so yeah uh so it will be
Chun Shao: Okay. I have a question.
Zhanfan Yu: Uh, go back to the previous.
Chun Shao: Sorry.
Zhanfan Yu: Yeah.
Chun Shao: Yeah. Okay. I have a question like uh Okay.


00:16:49

Chun Shao: You received the message you normalize payload. What what what do you what what do you want do in normalize payload?
Jude Pineda: explained here. Uh yeah so we load the application from documents list from the message uh with uh we deduke the documents list if there are any and so this just means a normalized partune uh so we flatten the application form to that part so for example application form owners owners 001 ssn so so for so it's easier for us to match this uh string here since this asteris here will be just a wild card for the ID of the owners. Uh, does that make sense
Chun Shao: Okay. Um, yeah, about this uh owners, I have another idea. If you can scroll up all the way to the popsup messages. Yeah, look at this one. So, uh, like the document list, you have the ID of the document, right?
Jude Pineda: documents list?
Chun Shao: Yeah.
Jude Pineda: Yes, John. This is the ID.
Chun Shao: Yeah. Yeah. You have ID.


00:17:58

Chun Shao: Why not? We cannot have ID for the owner. The owner. Uh, no, it's not ID. Uh yeah in our design we don't have uh ID there. Okay. Um is address yeah address here address uh in the data schema uh how we store the owner is it stored like a separate table because we are using SQL right we are not using the
Adrees Muhammad: Yeah.
Chun Shao: we're not using mongo
Adrees Muhammad: Yeah. Correct. We have a separate table for the owner and for the owner address we have another separate table. So we have two tables for the owner.
Chun Shao: Okay. So if that's the case, so the owner will also have owner ID and with the owner ID we can solve a lot of problems.
Jude Pineda: Yes, June. Uh, owner owner 01 here represents the ID.
Chun Shao: Yeah. Yeah. So like uh in this creation uh okay first document list okay and uh you have a bank statement so it's like a all right so for document list should be a array right it should not be an object uh no no you okay ah because it's a stipulation okay so for the owner okay let's do is owner.


00:19:32

Chun Shao: Don't use owners. Use owner underscore list. Okay.
Jude Pineda: Uh I I was just actually basing this on the table tune because the table name was owners or owner.
Chun Shao: And it array. Yeah. What?
Jude Pineda: I think it was owner the table name tune uh from the database.
Chun Shao: Okay.
Jude Pineda: So I was thinking because uh there will be time that we need to update the record soon right for example uh the FICO score if there's like uh credit report for that specific owner so we we have to update this record right Right.
Chun Shao: Yeah. Um, just do what I told you. Okay. Owner underscore list address. If database is not designed like this way, do that. Okay. But okay. Database table name. It should be fine. Okay, owner. It doesn't need to be list. But if there is any in JSON format, okay, message or data, if it's a array, you use list because sometimes it's it's very hard uh to distinguish between plural or you know a single.


00:20:40

Jude Pineda: Okay.
Chun Shao: Okay. And make it uh array. It's not an object. So after the owner's list, okay, change the parenthesis to array.
Jude Pineda: Oh, we have the ID here, June.
Chun Shao: No, no, no, no, no, no. Listen to me. Change it. Change it to array. Yeah, I'll tell you what to do. Okay. Okay. Yeah. Just keep one. Yeah. Just keep the left parenthesis. Delete the right parenthesis. I keep all this. Yeah.
Jude Pineda: Okay. No, I'm sorry.
Chun Shao: Okay. Yeah.
Jude Pineda: Yeah, I get sorry.
Chun Shao: And delete this one. Okay. And uh next one is Yeah. Okay. Uh change the owner underscore001 to uh owner_ ID. Yeah. And put a fake ID there. Remove the parenthesis and put a comma after it. Yeah. Remove the Remove the Yeah.
Jude Pineda: What?
Chun Shao: Yeah.


00:21:51

Chun Shao: Put a fake Yeah.
Jude Pineda: This
Chun Shao: Put a fake ID there. Maybe quote uh owner uh underscore1. Okay. Yeah. And uh yeah, align the next three fields with the owner ID. Yeah. Um yeah I think uh okay remove the next uh okay move down your uh yeah move this line no next next line next line next line next line yeah move remove no no not this one upper
Jude Pineda: Answer
Chun Shao: yeah move yeah remove yeah so this is you think this can work.
Jude Pineda: question.
Chun Shao: Yeah. Do you think this can work? Like a owner list, we have owner ID there. So uh and we have like a first name, last name, SSN. So you do not need that uh star in your uh like a compare. You just keep like a owner list first name or owners list. Owner list. SSM and uh which owner need to be done is based on this owner ID.
Jude Pineda: Okay. Okay.


00:23:17

Chun Shao: Okay.
Jude Pineda: Sure.
Chun Shao: So it could be like a first owner uh has updated the name and the second owner has updated SSN. So this in this way we can we can separate just like a documents. Yeah. Okay.
Jude Pineda: Oh, is this okay now?
Chun Shao: Yeah, I think this this is okay now, right? Other people you have any suggestion?
Jude Pineda: Oh. Um, no.
Chun Shao: Okay. Uh to make it more clear, uh copy the owner list to the uh updated underwriting message. Okay. Yeah. Okay. And uh make owner O2 in the list. So make it two items of this array. Yeah. O2. And remove the first name, last name. Uh only keep SSN for O2. Only keep SSN for O2. Yes. And uh remove SSN for 01. only keep the first name and last name. Yeah. For all one. Yes. Okay. Yeah.


00:24:44

Chun Shao: So in this case they can know okay update it could be different but we have this ID to indicate it. Yeah. Okay.
Jude Pineda: Oh, it's okay.
Chun Shao: Yeah. All right.
Jude Pineda: So yeah we so this is not the case anymore. So we just uh I think this logic will not be not apply anymore.
Chun Shao: Okay.
Jude Pineda: So yeah.
Chun Shao: Okay.
Jude Pineda: So we just go to the next And we read the for all the yeah triggers are here this for example
Chun Shao: Update it later. Yeah. Okay. Get all purchase processor from underwriting. Okay. And what do I do next? Next processor. Read the tri. Okay. Mhm.
Jude Pineda: and then so yeah we build record set so basically this is just for the matching uh if there's uh if it if those triggers have been triggered so I have been fulfilled.
Chun Shao: Okay.
Jude Pineda: So yeah, if there are any matches, just a single one. So we add it to the execution list and if it doesn't, so we just keep it.


00:26:03

Jude Pineda: So if there uh so it's it's going to be run for all the processors, then we end it.
Chun Shao: Okay. Yeah. Okay. Scroll up a little bit. Okay. Build required sets. fields stipulations match documents list stipulation.
Jude Pineda: So yeah because we have two different kinds of uh for triggers tune right we have like a document triggered and the application form triggered yeah so that's why I have to processes here.
Chun Shao: Mhm. Okay. This one is uh okay a little complicated. match application form keys and the match document list stipulation. Oh, so all right. I kind of Okay.
Jude Pineda: All right.
Chun Shao: Uh I can understand. Okay. The flowchart. Well, uh I think it's it's okay. Uh even though there is like a like you separate actually you can you can combine these two but it's fine. Uh we can understand and uh yeah it should work if you follow this. Um yeah. Mhm.


00:27:24

Jude Pineda: So we're going next.
Chun Shao: The idea is like yeah when you add to execution list just keep in mind yeah some like u this docu some ex uh processor will generate multiple executions. Okay. And uh Yeah.
Jude Pineda: Yes, Jun. We have that here John CH.
Chun Shao: Okay.
Jude Pineda: Uh so for the processor execution processors execution uh for the filter processors uh this is how it's going to be uh executed. So if that uh application property type of uh I mean application property triggered type of a processor. So it's going to have a single execution and for the document triggered uh for example for driver's license uh processor we only spawn one docu uh one we only spawn one execution so we ignore the count of documents but for the blank bank statement since it's per document uh we count uh we count how many documents it is and so we have to trigger that specific number for its execution. Sure.
Chun Shao: Okay. Well, um I understand. Okay. But the better way is not to draw like this.


00:28:45

Chun Shao: This is still like a uh you have like this field processors. The better way is like a process execution is you start and you have a list of executions and you run them parally and then after all completed you aggregate results. Okay. If you go up if you go up view yeah this one you can see you have a execution list right add to execution list. So what you will do as a result is you get a list of executions and here yeah here you should draw this one uh as like a executions.
Jude Pineda: Oh, okay.
Chun Shao: Okay. So it doesn't have any difference from like either this is application triggered or document triggered doesn't make any difference. You just have this uh execution uh list and uh run parally wait all being completed then aggregate the result and for this like application triggered or document trigger you can you can move this you can copy this if you want go up you can copy this uh to go up okay Um write uh after any matches if any matches yes and you put this this there okay we can say okay whether this is a attribute like a trigger or document trigger document trigger it's like whether it's like the processor is uh based on stipulation uh one exclusion or based on document will be multiple exclusion so you add to


00:30:36

Chun Shao: docu execution list okay You understand?
Jude Pineda: Oh yes. Basically this just have to be moved uh to this part.
Chun Shao: Yeah. Yeah. Similarly. So, um Yeah. Because you you you you already get like a Yeah. Okay.
Jude Pineda: So for the aggregation uh I think yeah uh I think we have to start from the processor execution which has been completed.
Chun Shao: Mhm. So, aggregation is uh Oh, hold on one second. So the event is uh deletion event.
Jude Pineda: Uh this is uh for individual indic ex execution. So first we save the execution data uh including it factors delta status uh I'm sorry about this timing I have to delete that in the uh processor execution table and then we have to uh so yeah this is
Chun Shao: Okay.
Jude Pineda: just actually uh from what I have thought Yes, sir.
Chun Shao: Okay, first look at uh hold uh you look at the events. Okay, I I think you you can delete all the events. All right, let me explain to you.


00:31:50

Chun Shao: Okay, you have three uh one is deletion event that means there no execution. Okay. And the the second is process execution completed per individual execution. Okay. And uh so this one you what you will do is save execution factor data everything and uh then you go to processor. Why you go to processor execution again? Oh the database. Okay. Save to the database. And what's the next is what's next? Can you go down?
Jude Pineda: So the next thing is actually to when all of these uh individual executions are completed, we go to this event uh which will uh call active execution and then We aggregate those results and then we insert it per factors and yeah that's basically it
Chun Shao: Okay. So first like at the end of execution this database operation should be completed like the processor execution. Okay. Uh this database should be uh inserted already. You should not put outside of the execution. Okay. For each processor, the function execution function should include the writing into the database.


00:33:25

Jude Pineda: Yes. Yeah.
Chun Shao: Okay.
Jude Pineda: Uh Adrisad told me that already actually, but I don't have time to update the document.
Chun Shao: Yeah. Okay. Yeah. And uh Okay. And let me see. All processor finished. What do I do? All processor finished. Okay. Uh, scroll down a little bit. So, collect active executions. Okay. Um, all right.
Jude Pineda: So my idea with this June is actually just to uh instead of the so yeah my this is my initial design actually uh this is going to be changed actually.
Chun Shao: Um. Mhm.
Jude Pineda: So I just want to explain this uh instead of storing the factors uh individ individually during execution uh my idea here is just to store those individual factors uh when all of those uh processors have been finished.
Chun Shao: Yeah.
Jude Pineda: So we can aggregate it and that's the time where we store it.
Chun Shao: Okay. Okay. Yeah. Okay. Go.


00:34:24

Chun Shao: Go up. Uh can you go up? Yeah. Uh go up more. Okay. Now this is uh how to say this is uh what card this is you get a list of all the executions. Okay. And uh if you can go up can you go up more? Go up the the previous Okay. Yeah. Um okay. So if you look at this this chart um when you receive message you normalize payload and the selected processors. Okay. Um I ask you a question what is manual or by triggers.
Jude Pineda: So from manual from the API tune um from figures is obviously this is mean the filtering part this one.
Chun Shao: Okay. So if it's from API um okay all right yeah all right okay okay it could be a little bit confused because even if it's by API is still like a message received okay but anyway okay you select processors
Jude Pineda: Yeah. Yeah. If it's manual then it will just bypass the filter tune.


00:35:46

Chun Shao: now remember you have a list of processors okay you will have a list of selected processors okay and Then you what you will do is you will um okay and you will have another list
Jude Pineda: Yes, we Oh,
Chun Shao: of executions. Actually you will have two lists. One list is processor list selected processor list. One list is execution list.
Jude Pineda: okay.
Chun Shao: You understand? Yeah. The processor list could be like a um based on these uh uh parameters. Okay. Any fields updated you have like maybe three processors but the executions could be like a five because one processor could have three executions. Okay. So you have two lists. All right. Then you execute filtered processors.
Jude Pineda: Yes.
Chun Shao: Actually, it's better to name it like a execute the uh ex okay perform the execution. Okay, perform the execution. Okay, and uh after the perform the execution, you aggregate the result. Okay, when you do this uh execution, it's based on the execution list.


00:37:15

Chun Shao: And when you do the aggregation, it's based on the processor list. So you can you can yeah uh you can put parenthesis uh if you can go up. So perform execution uh space per uh uh per ex uh like a per execution list. Okay. All right. And the aggregate result pro per processor list. Yeah. Okay. So let me explain to you what will happen. So um if they delete anything, okay, there will be a processor list maybe one processor but there will be no execution list, right?
Jude Pineda: Mhm. Oh, okay. Yeah.
Chun Shao: uh all probably there will still be a execution list. Uh how to handle that? Like you need to mark the previous execution to be disabled. Okay. But anyway there will be no new execution. Okay.
Jude Pineda: Yes.
Chun Shao: Uh no no no no you it's not in the API it should be in your processor you should find a place to update it okay um


00:38:34

Jude Pineda: Uh if I'm understanding it correctly, uh address uh should that be handled by the API during the deletion or does it have to be executed inside the processor model?
Chun Shao: okay anyway so let let's just say there will be no new execution so the execution list will be empty but the processor list will have one item. So the perform execution will actually do nothing but it will do the aggregation again. All right.
Jude Pineda: Okay.
Chun Shao: So yeah these two pro these two list you know the difference one is like
Jude Pineda: So for examp uh for example J uh if there's a bank statement deleted uh March. So since there's a deleted I have to run the execution for all those existing documents right or not. I did I understand your point correctly?
Chun Shao: no you don't need to run you don't need to create any new execution you just yeah you just yeah you need to aggregate based uh you need to aggregate the um how do say the bank statement processor again
Jude Pineda: I am sorry. Aggregate the


00:39:55

Chun Shao: and when you aggregate it because previously for example you have three bank statements uh result and you because you delete one document then there will be no new execution but this the previous execution will be marked as deleted.
Jude Pineda: Aggregate.
Chun Shao: So when you run the aggregation it will aggregate everything and uh and it's based on the two uh previous execution result which remains enabled and will eliminate the uh deleted execution result from its like uh uh it's its uh source to generate uh different factors. Okay.
Jude Pineda: Yeah.
Chun Shao: So uh Mhm.
Jude Pineda: Does that look like this, June? Uh I'm sorry. Does this does that look like this? For example, we have the deletion event and then we just get all the um non nondeed executions. For example, uh does uh do we have to aggregate then and then we store the factors? Uh does it obey this?
Chun Shao: Okay. This uh flowchart is for the execution, right?
Jude Pineda: Uh it's for the aggregation June data add for the yeah


00:41:04

Chun Shao: Yeah. Yeah. Okay. So, uh yeah, probably you can you can modify this to handle. Okay. Um how to do that? Okay. Because the message you received it will be a document list and it will be a stipulation bank statement. And uh in the bank statement there will be a delete and uh the delete has an array with a document ID.
Jude Pineda: Yes.
Chun Shao: Okay. When you received this kind of message so you will find out okay you flat the uh path of the JSON file. So you get document list dot um the bank statement uh and you will say okay I will add this processor into the processor list all right and then because it's delete so you need to handle it differently from create and update uh to mark the previous execution as deleted Okay. As previous execution result as deleted or the the status. Okay. So you need another like a maybe where you should put it maybe maybe in another like a uh yeah another flow chat to mark this or yeah it's not it's not like you create in uh


00:42:40

Jude Pineda: separate uh charging. Okay, this is not an equation.
Chun Shao: create a execution it's like you mark
Jude Pineda: So this is just for the aggregation part. This one here, there's no execution for this part. Uh executions are inside here. So in the aggregation part, we just insert the per factor rows based on the previous uh executions. I have not only based on previous executions but based on the which are which executions which exe execution results are active.
Chun Shao: No, it's okay. So when you do the aggregation, it will be very very simple. So just aggregate factors based on active executions.
Jude Pineda: Yes.
Chun Shao: That's it. Okay.
Jude Pineda: Yes.
Chun Shao: Yeah. And uh yeah, this is just okay. The okay almost looks fine. It just you need to find a place to handle uh the uh like a not new execution but update the previous execution and my suggestion is you put it into the flowchart of processor filter. Okay. You have a flowchart processor filter chart.


00:44:06

Chun Shao: Yeah, this one you should put it somewhere here. Okay, like here it's it's like a add to execution list or skip. Probably you will have another one like to mark uh previous execution invalid.
Jude Pineda: Okay.
Chun Shao: Yeah, probably we need to add one here. Okay.
Jude Pineda: Okay. Sh.
Chun Shao: Yeah. So you will have a list of processor, you will have a list of execution and if there is any deletion uh the execution list will be zero but the processor will keep remain there and based on the processor you can run the aggregation.
Jude Pineda: Okay.
Chun Shao: Yeah. And so for this aggregation it will not be so complicated. You can remove all the events. It's just a per processor. It runs. It runs. Okay. You don't need to care about any like a well is it triggered. You just start and uh get the first will be get all the uh valid or active executions and then is generate factors and then write to the database and that's it.


00:45:35

Chun Shao: Okay, not that complicated. And uh this uh like uh uh write to the execution uh process execution database right into those database uh that should be inside the workflow of uh execution. Okay. Flow workflow process execution workflow. Yeah. It will Okay.
Jude Pineda: Okay.
Chun Shao: So separate separator. Okay. Yeah.
Jude Pineda: Uh so just my question tune uh since we're going to uh aggregate results uh that's going to be outside the execution, right?
Chun Shao: Yeah.
Jude Pineda: So uh how are we going to like uh wait let me check this question.
Chun Shao: Oh, by the way, did Philippine have a earthquake couple days ago from your area?
Gene Rellanos: Uh yes, but it's far from our uh far from our region. So we did not Yeah. Not our area. They're not yet affected by by much for me.
Chun Shao: Okay. Okay. your f you you have any friends family in the restrict area.
Gene Rellanos: Nope. Uh how about you dude?
Chun Shao: Okay.


00:47:01

Gene Rellanos: Do you have a
Jude Pineda: Oh no, not actually here. Uh so yeah the question raised by address was uh uh how are we going to def are we going to create a new table for the aggregation so that we can uh maybe link it to the factors or what is it necessary Also,
Chun Shao: No, it's not necessary. You don't need a table for aggregation. You just uh okay, you have all the executions and uh you get data from execution table and uh aggregate it and write to factory table. That's it.
Jude Pineda: if that's the case, if we're going to um Oh, okay. Never mind. I get it now. Okay.
Chun Shao: Mhm. Yeah. So if in this workflow chart you want to include the processor execution uh table um it's should be read only like a read from this execution table and uh doing some process to find out the factors and write into factors table and that should be yeah that should be it. Okay.


00:48:18

Jude Pineda: I think kitchen.
Chun Shao: Mhm. Yeah. Okay. Um, yeah, pretty much that's it. Jeremy, you have any comments?
Zhanfan Yu: Uh I will review the design details please.
Chun Shao: Okay.
Zhanfan Yu: Yeah I don't have question per.
Chun Shao: Okay. All right. So, you also understand, right? The uh the execution is based on execution list. The aggregation is based on processor list.
Zhanfan Yu: Yeah.
Chun Shao: Okay. A race. Whoa. Whoa. Whoa.
Adrees Muhammad: Yeah, Jun. Uh, I want to show you the schema like uh I have updated it. Jude, can you go to the schema part? Yeah. The processor execution. processor execution. Yeah, this one. Okay. So, uh previously as we discussed uh we have we can have multiple document uh documents against one execution and we can have one document or we can have no document against that execution and uh we need to uh manage the history of the execution as well.


00:49:53

Adrees Muhammad: So for that I have added uh three properties. First of all, I have added a document ids. So in that I will save the uh document revision ids which like the documents which we used to perform that particular processor execution and uh the next property is document ids hash.
Chun Shao: Mhm.
Adrees Muhammad: It will be the hash of those ids so that uh we can uh like calculate the similarity. Okay. So the last on the last we have updated execution ID. This updated execution ID will store the updated ID of the execution against that particular documents. Okay. So let's say we have a driving license. First we process two documents uh front and back. So we will have a document ids two document ids in document ids and uh then we will calculate uh its hash on the just ids hash and uh then we will save the let's say updated execution ID for now is null okay so it's the updated execution against the driving license so next uh if the user reupload the driving license or change something so we will have a new document ids and uh we will have a new hash And uh the updated execution ID now will be null but the previous uh for the previous execution we will have updated execution ID to the current one.


00:51:27

Chun Shao: Okay.
Adrees Muhammad: So is the ID is correct?
Chun Shao: Yeah. Yeah. Correct. Okay. Just one thing like uh uh everything if it's a list don't use s. Okay. Use a list. All right. This is one thing and the second is uh well where you can get the where you get this hash is like based on the content of the document or what?
Adrees Muhammad: Okay. Okay. Okay. No, just the ids. We don't need to calculate the content because we the ids are unique.
Chun Shao: Uh okay. So this is for what like to compare whether any change on the document.
Adrees Muhammad: So it's uh the purpose of it like uh is to compare when we last uh execute uh the driving license where the processor against the driving license. The purpose of it so so that we can maintain a history of the execution of the driving license. Let's say you can say that. So it's basically against one stipulation type or Yeah.


00:52:36

Chun Shao: So when it will be used for like this hash
Adrees Muhammad: So the updated when when I want want to change the updated execution ID property then I will use the hash so that I can uh link the those which uh which are connected and when let's say I want to uh get some executions from that table so using that hash we can distinguish Uh the types of the uh documents we have executed.
Chun Shao: Okay. All right. Yeah. Because this execution is a little bit tricky. It's not like a factor. Okay. Each factor based on this factor ID. Okay. or factor key name, it's always this one. But this executions could be a little bit more complicated because one processor like sometimes it's not only one active execution. Uh it could have multiple and it's based on like for now it's just based on document. Okay. Um yeah, your design is good. Okay. It's not based on Oh, all right. Um, SQL doesn't support array type, does it?


00:54:03

Chun Shao: Or like this is a Google query.
Adrees Muhammad: Post Post S Postport the array.
Chun Shao: It it supports array. Ah, okay. All right, then that's good.
Adrees Muhammad: Yeah.
Chun Shao: Yeah, I have no other issues. So, uh, okay. Uh, one second. document revision ID. So what you save is the document revision ID. So this is for what in case there is an update of one document even though the document ID doesn't change the revision changed.
Adrees Muhammad: Yeah, we saw document ids here.
Chun Shao: Uh yeah.
Adrees Muhammad: We are storing the document review and ids here.
Chun Shao: Okay. So when you do the harsh of the document, you will make sure you use document ID, not use document revision ID.
Adrees Muhammad: like we uh in the rev uh the purpose of revian is to store the multiple uh documents if the user reupload that. So here I want to store the document review id. So I have mentioned the type of that document ids as a revian ids array.


00:55:25

Adrees Muhammad: Can you uh can you go back? Can can you walk? Yeah. So uh here I have mentioned the document ids type as document revision ids array. So it will be array of document revision ids not document ids. Uh the purpose of revian ids is basically against one document we will have multiple revian. We need a specific revision of that.
Chun Shao: Yeah.
Adrees Muhammad: That's why I added
Chun Shao: Okay. Okay. And uh so I just remind you that the document ID's hash should be based on document ID not document revision ID otherwise you will not be able to track the history. You understand what I'm talking about?
Adrees Muhammad: Okay. So it will be like uh in case of document ID it will be specific to the stipulation and and type.
Chun Shao: Okay.
Adrees Muhammad: That's what you mean like
Chun Shao: Okay. Let me let me give you an example. Okay. You have a bank statement. Okay. One bank statement and you use a bank statement processor and you get a execution.


00:56:46

Chun Shao: Okay. So you have this document revision ID and you have this hash. Okay. If the hash is based on the revision ID and they upload a new file to override the previous bank statement and uh it will get a new revision ID but the execution should be uh on the same document right so the next uh execution should override the previous one and they should share the same document ids hash to locate uh that under this bank statement okay this execution the updated execution is override the previous execution uh by the same document id's hash but if you use the document revision ID to do the hash you will have a problem you will have a different values and you cannot find the previous one or even if you can find but like this ID hash will give you some trouble. Okay? You understand what I'm talking about?
Adrees Muhammad: like we perform the execution based on document revision not the document the purpose of the document is to just store the uh properties which are common in the pro document revisions like it's a stipulation type or something.


00:58:13

Adrees Muhammad: So we perform the execution on the document revision itself because we have a uh we when the user reupload the document then it uh become a new revision then we process that particular revision. We not process the document here.
Chun Shao: Yeah, but I I I mean okay how if I there's if there is a new execution and update the previous one, how you know that the which record you should like update the updated uh execution ID? Okay, it's based on first which tenant, second which underwriting ID, third uh is the processor. Okay, based on this three or you can just based on like the underwriting process ID. Okay. And uh but there is one more thing is for the bank statement is it could have multiple. Okay. If it has three documents, it has three records in the database of this execution process execution and which one you want to override it like update the updated execution ID. You should have a extra because they share the same underwriting process ID. So you need to have an extra field to identify which one which execution.


00:59:41

Chun Shao: So it's based on document ids hash. Is that correct?
Adrees Muhammad: I'm a bit confused now but uh I guess it's uh like the document revision will have the latest ID of the latest document which we have currently.
Chun Shao: Yeah.
Adrees Muhammad: So we can use its ID with Okay.
Chun Shao: Yes. Yeah. But it's keep changing like for the same document ID it will have it it will have different document revision ID.
Adrees Muhammad: So you mean if user change the document, how will I enter that part in processor execution?
Chun Shao: Okay. Let's say document ID. Okay. Let's say you there is a document ID is one two three. Okay. Doc one, two, three. And you have a revision ID is ABC. The first revision, the second revision is DEF. Okay. If you use ABC to hash the document ID, it will be a problem because the second uh update is DF is different from ABC. They have this different hash code. You cannot find which two documents are actually the same document.


01:01:04

Chun Shao: You have to use document one two three as the ID to be hashed. So even DEF is changed or ABC is changed to DEF but they share the same one 123 document ID. You get it?
Adrees Muhammad: Okay. Yeah.
Chun Shao: Uhhuh.
Adrees Muhammad: Yeah, I got it.
Chun Shao: Yeah. So it just remind you you what you put there is correct document ids hash strong hash of document ids I just remind okay okay remind you remind Jude uh genie that this should be used um should use the document ID not document revision ID as you are going to store there the document ID s use that revision ID to do the hash.
Adrees Muhammad: Okay.
Chun Shao: Okay, you you understand? Did uh J understand about that?
Jude Pineda: Oh, yes.
Chun Shao: Okay.
Jude Pineda: I got it.
Chun Shao: Yeah. Okay. What you write in the comments is correct. Okay. Okay, I just want to emphasize it. Don't mix with this. Okay. Storing ids of all the documents against which the current Yeah, because you put a revision there. So, yeah, they will know this is a revision ID, not the document ID. Okay.
Adrees Muhammad: Yeah, put
Chun Shao: All right. Okay. So can you can you show me the definition of document revision like the the table. Okay. Yeah, it has its own ID and it keeps the document ID. Okay. All right. Sure. Thank you. Okay, that's it, I guess. Um, yeah. Can we meet again tomorrow?
Jude Pineda: Uh, okay.
Chun Shao: You up, you update the flowchart, workflow chart.
Jude Pineda: June.
Gene Rellanos: question.
Jude Pineda: Okay. Same time, June. Okay. Uh, thank
Gene Rellanos: Thanks See you tomorrow.


Transcription ended after 01:05:17

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
