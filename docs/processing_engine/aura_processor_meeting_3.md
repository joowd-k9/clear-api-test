Oct 3, 2025
AURA Processor - Transcript
00:00:00

Jude Pineda: Uh good morning again guys. So, I guess we'll have to wait for Chin because he said uh he's in another meeting and he'll join once he was finished.
Gene Rellanos: I'm big.
Jude Pineda: Uh also, uh Adris, can you go back to the documents hashing you mentioned earlier?
Chun Shao: Hello.
Gene Rellanos: Hello. Good morning.
Chun Shao: Hi. Morning. Sorry for late. Okay. All right. Let's check.
Jude Pineda: Good morning.
Chun Shao: Yeah. The money. Let's check it. Okay.
Jude Pineda: Okay, J.
Chun Shao: Yeah. Can I share the screen?
Jude Pineda: No. Okay.
Chun Shao: All right.
Jude Pineda: So yeah I have updated the uh high level vion. So this one I have separated the path for uh manual execution.
Chun Shao: Mhm.
Jude Pineda: So it just direct just directly go to the build execution list.
Chun Shao: Okay.
Jude Pineda: And then I also have added uh uh the invalidation path for uh for if there are if there are any deletions or revisions have been triggered.


00:11:45

Jude Pineda: So yeah if that happens uh we have to invalidate uh prior executions. So after after those two uh we didn't have to aggregate and then update existing factors. So for the detailed overview here uh so okay
Chun Shao: Can you go up a little bit? Sorry. Okay. Yeah. Yeah. All right. Get purchase the filter processor by triggers. Okay. over on the right side when it's trigger like execute a certain processor or yeah just uh remember to like also build a processor list on your right side the one that execute the processor directly from API.
Jude Pineda: Uh, I'm sorry to Can you repeat that?
Chun Shao: Yeah, if you scroll up a little bit now, it's like you separate these two uh from two groups. One is like underwriting update or created is on your left side. Okay, on your left side you have like a one part is a future processor by triggers, right? And then you can get a list of the processor and you can do the aggregation.


00:12:53

Jude Pineda: Yes.
Chun Shao: And uh on the right side you said okay message received manual execution and the parse row payload and uh build execution list. So um uh but don't forget like uh on the right uh workflow you also need uh maybe in one process you will say okay uh build this uh processor list something like that. So in the aggregation you will also have a list of the processor that they can do the aggregation.
Jude Pineda: Oh, okay. Yeah, that makes sense.
Chun Shao: Yeah, yeah, yeah, sure. And uh Okay, looks good. Uh any deletions? Okay, sure. Um yes. Okay, good.
Jude Pineda: So yeah, I have more detail here. So we have the filtration which is uh the same as yesterday. I just made it simpler and yeah I have separated both uh invalidation and executions here tune. So yeah for the for the executions.
Chun Shao: Uh, okay. Can you go up? You're too You're too fast.
Jude Pineda: Okay.
Chun Shao: Okay. I'm an old person almost 50. So, I'm slow and please be slow.


00:14:18

Chun Shao: All right. So, what is the first one? Filtration.
Jude Pineda: So we have to get the purchase processor and then iterate through each uh purchase processor.
Chun Shao: Okay. Um, yeah.
Jude Pineda: So first is we have to check if it is if it is a auto automatic execution or is it is it enabled. So yeah if if if it yes so if it's not then we just uh skip it or exclude it.
Chun Shao: Okay. Auto and enabled. All right.
Jude Pineda: So if it's yes then we have to read the trigger so we could match it. If there are if there are any matches we just have to add it to the processors list.
Chun Shao: Mhm. Okay. All right. Um, yeah, the way you draw like uh you make it too complicated because it's like a loop. So this four per for each purchase process actually this becomes a loop. Okay. And uh for the flowchart we uh I don't know whether we should keep it that that detail but for me like uh it's you you can make it very simple like uh get purchase processors and then uh filter out uh auto and enable.


00:15:31

Chun Shao: Okay. All right. And uh then it's like uh read the triggers because you already filled out the uh auto and enable then next the read the triggers. So uh if any is there any match and uh and added to the processor list. So it's like a strict uh you don't you don't need to have so so many loops. Okay. The purpose is yeah the purpose is to filter out the processes that's not okay in the list.
Jude Pineda: Okay. Check.
Chun Shao: So first you get all purchase processes next you filter out uh by the auto uh by the enabled okay next you filled out by the auto next you filter out by the trigger and uh after these three steps how many processes you left and those are the processor list. Yeah good. Okay.
Jude Pineda: Okay. So I'll have to update.
Chun Shao: Yeah. Yeah. Yeah. Yeah.
Jude Pineda: So so I after that we either go to invalidation or execution. First is we try to look at this uh executions.


00:16:36

Chun Shao: Mhm.
Jude Pineda: So yeah for each uh same thing we have to look so for each for each processor in the processor list here.
Chun Shao: Mhm. Yeah. Yeah. Uhhuh.
Jude Pineda: So we have to check its match type. So yeah first if it's a application we add a single execution to it for that specific processor. And if it's a document then we check its execution mode. If it's a single document regardless of how many I I mean I'm sorry we check the execution mode uh if it's single meaning uh we have to make a single execution regardless of the document count. So yeah, we have to add one execution to the executions list for that specific processor. And if it's per document, then we add n number of executions to the executions list.
Chun Shao: Mhm.
Jude Pineda: And after we're done, we have the executions list. And then we perform parallel executions for processor in executions.
Chun Shao: Yeah. Okay.
Jude Pineda: Yeah.
Chun Shao: Okay. Basically, yeah, basically I think you can hard code this part like uh when I talk about hardcode, you can uh switch by the uh type of the processor by the processor key.


00:17:37

Jude Pineda: And then
Chun Shao: Okay. So it's like a if it's a processor P application uh like processor like a processor application or it's a processor industry or processor something they are all based on the application form data and doesn't include any documents then you can call on their execution with particular like a u it just called with the probably the underwriting ID that's it and uh if like for example it's driver license P driver license it's another kind that you pass by the underwriting ID and you don't need any docu uh uh probably you can pass the document list okay it will record uh recorded as records but anyway it will check all the documents okay and there is another one is uh P bank statement this is very special one. So you will create multiple executions uh you based on the document ID you break it down. So if it has four or five then you create four or five different executions and put in the execution list. Yeah this is uh uh this is yes. So you you can hardcode it this part.


00:19:14

Chun Shao: It like the way you designed is um is good uh but this is good for like a if you will have like a many different uh types of u processors. Okay, that will be increased and will be added to the system uh like frequently. But what we have is like uh to write a processor may take one or two weeks to have one process to be add on and once we have like a uh 12 15 processes pretty much uh the processors we we provide is fixed. Okay. So that's why I said this part you can hardcode it. Yeah. But but fine. Yeah. The the idea is is like that. This is what we want to do. Okay.
Jude Pineda: So yeah uh then we have we can switch to the and validation part. So yeah for each uh processors we have to look it again. So first is we have to check if there's uh any deletion or revision there. So if that's the case, we have to check for that individual ids and then get get its uh processor executions and then we add that to invalidations list and then if it's not so we go to no here and if it's a created attribute with uh with that processor that is specific for uh only a single execution.


00:20:44

Jude Pineda: So based on your example on a previous meeting as Adris have uh as Adris and I have discussed earlier that we can have only one execution regardless of how many documents right. So we have to get that processor executions uh the previous ones then we add that invalidations list and after that we invalidate all those executions and its and its factors.
Chun Shao: All right.
Jude Pineda: Uh is this flow correction?
Chun Shao: Okay. Um I think we can Okay. Make it simple. Okay. Don't do this uh uh invalidation uh of like update here. I I can give you the reason why is it could be failed for new execution. All right. So if the new execution is failed um we should keep the previous execution result. Right.
Jude Pineda: Mhm. Yeah.
Chun Shao: Uhhuh. Yeah. Uh okay so did then we will have a problem okay now we have a problem so let's say we have a document and uh they par like a bank statement okay they passed and get a result and get


00:22:02

Jude Pineda: Okay.
Chun Shao: a factors now they upload a document to override this one and we have a like a overwrite update document okay but this document the file is corrupted So they have a created a new execution but this execution failed. So what do we should do?
Adrees Muhammad: I think uh the uh to update the uh details in the database it will be done after the execution is successful. If any of the operation is failed then it will be reverted. So it will be like in an transaction we will have a transaction in database query where we will perform different queries uh in sequence. So if one uh is failed then all the transaction will be failed. So in case the execution is failed so we will not update anything. Everything will be reverted and the previous execution will hold. It will be uh like uh the active execution the previous one.
Chun Shao: Okay. Um so like we have two options. First is we keep the field result. Okay. And we also mark the previous execution as like a deleted okay or updated and with the new uh result but the new result is like a field okay it doesn't matter I mean because you upload a new file you overwrite the document and now you get the result as field it's better than like you keep the previous one but that that result doesn't match with with the most updated uh document because the post updated document version


00:24:08

Chun Shao: two is a field one and execution is failed. So in in this case we can we can keep the field result as a result. So we doesn't it doesn't matter with the status of the execution either it's successfully completed or it's failed it it will overwrite okay the previous result. This is one way. Okay. And uh the second way is like if it's a failed execution, we will roll back to the previous situation. Um is that necessary like a should we do that?
Gene Rellanos: uh if we rolled back result but the file itself is already replaced right the old file is gone so if you roll back ah okay I see I see I see I
Chun Shao: The old file will not go. The old file will still keep there. It's just like Yeah. version one, version two, the document.
Gene Rellanos: see a mistake
Chun Shao: Mhm.
Adrees Muhammad: It's not about just the execution failure. We can have a failure in other phases as well like maybe in factors or in pre-check or other phases as well.


00:25:30

Adrees Muhammad: So we uh we can come up with a thumb rule like in case of failure we just keep the previous as corrected because the failure can like uh can make the results inappropriate or which doesn't make any sense to add that and override that. So it can harm our results not that sense.
Chun Shao: Mhm. Right. Okay. So make it simple we don't provide like a roll back function otherwise it will be very complicated too complicated okay because we need to like a switch we need to decide it okay which document if we roll back do we need to like a roll back also the documents and the version will be changed so if there is any failed execution and uh it will be failed and keep as failed unless they provide another document a correct document to override it. It will remain the field of the situation. Are you all agree with that? If we if we do like this way then it should be fine with the current workflow that is if execution failed we just keep it as is failed.


00:26:52

Chun Shao: We will not provide any roll back. So they have to provide a correct document or form data to perform the execution again until they get a like a success execution to generate factors and move forward. You think that's okay? Is it just pending for Yeah.
Jude Pineda: Um, I just have a question. Uh, why can't they have an option to maybe roll it back? Is there any like reason
Chun Shao: Yeah. This is like what I'm thinking uh previously like uh uh what if it's not failed execution? What if the execution is cancelled or something? it's not completed and uh you will mark uh the previous one like uh as uh as deleted or as like uh updated but it's fine like uh as long as you have a execution ID you can like mark the previous execution as updated okay but uh still uh like okay for deletion you can you can do that on your after side workflow invalidation because like a it's processor based uh and you provide if there is a document related you provide a related document ID uh but for like a there is a new execution I would like to keep this like a mark previous as um uh as invalid operation probably at the end of the execution once it's performed either like a completed or like um uh incompleted uh we can we can mark it uh which one is better


00:29:00

Chun Shao: oh probably your design is better because for example if we include the UI and when you hit the like a processor it already have two executions and one is uh deleted the second one is the active one and when you hit uh execute it. So before it's execution actually running it will create a execution record and uh it will mark the previous one as disabled or deleted and show in the UI show the new one you created but the status is not finished ready it's showing like u it's running so in this case you will know there is a new execution. Yeah. What what you did is correct. Yes. So separate these two. So even before the completion of the execution we as long as we have a execution list. Okay. We will mark the previous execution as updated with the new execution ID and the new execution can take maybe one minute, two minutes to run until it get a new result. Yes, we can do that. Yeah.


00:30:20

Chun Shao: Yeah, this this this design is good. Yes. Okay.
Adrees Muhammad: I have a question like uh uh uh what if the execution doesn't give any result in the case of failure it doesn't get any result or for some reason the execution stuck or for any reason the on the processor end let's say clear on clear processor and something happens we don't don't get any result as you said first we just create a new execution and mark the previous one as outdated while the new one is is
Chun Shao: Yeah. So Mhm.
Adrees Muhammad: in progress. So this use case will become like uh uh false I guess that's the problem in that case what we will show in front end we don't have any result in that scenario
Chun Shao: Yeah. So in this case, okay, previously we have a successful uh clear report and we get some factors and we have a result. Okay, intermediate result uh but the second run failed. So that means intermediate result is uh is empty or is a now object and uh then we run the aggregation based on the most up to date result and it's now so uh all the factors will be updated as now okay or be removed uh I don't know uh yeah as long as there is already factors so it will be like uh marked as the previous factor will be also be updated with new one as like


00:32:06

Chun Shao: a null value. So uh all the information we get previously we get um maybe they can pass the criteria checking pre-checking everything and now it becomes the data missing. Yeah, it will become data missing. Um unless okay now that looks like we need to provide something like a roll back. We can delete the execution and this deletion is uh like we break from the chain. Okay. So it will not like in the chain it will be included because the execution of one processor it's now we stored as a chain. Okay. The first one link to the second one. The second one link to the third one. Uh but now it will break out from the chin and keep the one uh in in in there. So yeah. So something like that.
Gene Rellanos: So, uh if we break the chain, do we do we uh see
Chun Shao: We still be able to find it out based on the underwriting ID, process ID. Uh yeah, we still be able to find it out in the database.


00:33:29

Chun Shao: It's just yeah, it's just not in the chain. And uh yeah, it will be marked as disabled uh but without updated processor info. Yeah.
Gene Rellanos: I see uh what if we in the processor uh processor execution list let's say uh let's say we have we separate the aggregation in the the processor execution like uh uh in the maybe in the UI there's a
Chun Shao: What?
Gene Rellanos: table where there's the processor executions and after they executed there's a result we can see. So if maybe if we don't like the result we can maybe mark this execution as a invalid and then we can and then we can proceed in the aggregation where the invalidated processors were not included.
Chun Shao: Uhhuh.
Gene Rellanos: So, so that maybe the data the data for that invalid uh processor will not be included in the final factors
Chun Shao: Yeah. So, you're right. So, like we might have a new uh API. Okay. Besides these three, there could be like the uh enable or like a disable the processor. Oh no, no, not processor, the execution.


00:34:54

Gene Rellanos: there. the result. Yeah. The execution result set up.
Chun Shao: Yeah, the execution result. So once the execution is set up.
Gene Rellanos: So you can set.
Chun Shao: Okay. Uh for example like we have uh two executions and the second one will uh replace the first one uh by default but then we find out okay the second one either is a failed or the result is not correct. Then we can okay right click on the first execution and choose okay we want to set this as the result. then it will reverse the uh chain link that the second one will be marked as disabled and it's update info will be the first one something like that. Okay. Yeah.
Gene Rellanos: Yeah.
Chun Shao: And uh then it will uh do the aggregation again. Yeah.
Gene Rellanos: Yeah.
Jude Pineda: Okay.
Chun Shao: So this this will yeah so this will be similar to the deletion okay of like a document this is like a uh disabling or enabling a execution.


00:35:54

Jude Pineda: So after that
Chun Shao: So but we we we will we don't care about like which execution has been enabled or disabled. It doesn't matter. We just do the aggregation. That's it. It's just like a rerun aggregation. So, so for that part, so for that part, yeah.
Jude Pineda: uh what was that June?
Gene Rellanos: Yeah.
Jude Pineda: We get the
Chun Shao: So, for that part, add the API will provide a function that is uh execution is uh updated. Okay, it's either enabled or disabled. Okay, and it will give you like uh which processor its execution has been updated. and you get this message. You call the aggregation for this processor directly. You don't need to perform any execution. Okay, you just call the aggregation function. This part the the lowest part of your flowchart directly from that API call. Uh yeah from that popsup message you receive from API which is uh processor execution like updated
Adrees Muhammad: from my question like uh uh should we keep like keep the failed execution or just uh use the previous active one.


00:37:38

Adrees Muhammad: So what we will do in that case
Chun Shao: Okay. So, uh we we still by default we keep the field. Okay. It could be filled. I mean like uh you you cannot say okay if it's a field Zen this is uh this is not not good. Uh sometimes we might need like a field. So we know okay they they provide the document is not correct we need them to uh provide a updated one okay so they can they can have failed value and uh this is the uh responsibility for the underwriter to like uh determine whether I upload a new document to get another execution or I can recheck and I found out okay it's mistakenly I uh Okay, they say okay I want to upload this document uh as a Javus license but I unfortunately I overwrite the bank statement. This is the reason uh it makes this uh execution run. So I can manually mark the previous one as execution as the correct one. Okay. And uh yeah, maybe we need to handle uh that also uh the the revision.


00:39:03

Chun Shao: I don't know like uh uh do we need to like uh also ask them all the we can allow them like manually to delete the document revision the second revision and keep the first one. um because execution is linked to a document and also a revision ID, right?
Adrees Muhammad: Yeah.
Chun Shao: Yeah. So when you disabled uh like a delete soft delete a execution all the related revision of the document should be marked as delete. Correct.
Adrees Muhammad: Yeah, correct.
Chun Shao: Yeah.
Adrees Muhammad: So, uh, regarding that, um, I have another question.
Chun Shao: Mhm.
Adrees Muhammad: So, I think we should clear that first. So, regarding the, uh, regarding mark the previous, uh, execution as deleted, it depends, it will depend upon the document hash property which I mentioned before. So basically uh what it means like uh if the uh let's say uh first a user uploaded a driving license with the front and back. Okay. So in in first execution okay we will get the result we will get the factors. Okay.


00:40:26

Adrees Muhammad: So if the user reupload the driving license front and back so it will be revision. Okay. So the document hash will be same. In that case, we just make the previous one as deleted and we will keep the this one. Okay, this is one scenario. Second scenario, let's say we have a second owner who upload a uh driving license with front and back. Okay, in that case we have different document ids. So in that case we will not make the previous driving owner driving license as deleted. We just add a new execution and we will just proceed. So is that correct?
Chun Shao: Hm. M uh can you say the question again? In that case we will not what Mhm.
Adrees Muhammad: like uh the deletion. Um we only delete the uh revision uh revised document uh uh like uh like we we only uh if the docu uh document list hash is same then we will uh make the previous uh execution as deleted. Do you understand that part?


00:41:42

Chun Shao: Ah okay. Now I understand. Yeah. Um yeah. So, so the the driver license processor even though it's it requires document but when it's uh maintain its execution list it will not use the documents ID hash as a criteria to find out the execution. So it will override it just based on the processor. So this processor will only have one uh active execution at one time even though they share different document ids hash.
Adrees Muhammad: So you mean whether we have driving license from two different honors, the execution will stay one.
Chun Shao: Yeah they will override it. the document ID, the document list hash will be different. But even though it's different, it will still be marked as disabled or updated. And uh the new execution ID will replace it.
Adrees Muhammad: Okay. Okay.
Chun Shao: Yeah.
Adrees Muhammad: So um as you mentioned in our previous meeting in that scenario we have a factor in the form of list. So how is that will be in the form of list if we have only one execution.


00:43:14

Chun Shao: Okay. So um let's say if we have uh one okay owner so the factor of the owner is an array which contains one item and then we upload two uh like a two more pictures. Now we have four pictures and the two owners and the factors will be a array with two items and will overwrite the previous uh the whole array will be overrided. Okay.
Adrees Muhammad: Okay. Okay.
Chun Shao: Yeah.
Adrees Muhammad: Okay. Yeah. Okay.
Chun Shao: So now let let me ask you a further question.
Adrees Muhammad: That
Chun Shao: What if they then deleted the second execution which contains two owner? Now we need to recover the first execution as available. Okay, that only have one owner. There's no problem. The factor will be overrided.
Adrees Muhammad: Yeah, we can do that. Yeah, we can do that.
Chun Shao: Yeah, will be overrided. But for the document this is so like a what are we going to do with the documents? Um yeah, if they upload Mhm.


00:44:22

Adrees Muhammad: Yeah, that's a scenario and I have another scenario. Let's say uh he has uploaded all the four documents at once. How you will identify these are two owners or how you will separate that part.
Chun Shao: Okay. Um I will say this. All right. Uh this is this will be based on the document revision ID. Okay. uh if they upload two image file for one owner the first time they have a revision ID for each document and these two re document revision ID will be including the first exclusion and then when they uploaded another two documents so the other two documents uh revision will be included in the second execution. Right now my question is what about the first two image their document revision ID will it be included in the second execution?
Adrees Muhammad: Yeah, it will be included.
Chun Shao: Okay. So when we mark the second execution as disabled and enable the previous the first one we we should mark the full document revision ID as disabled.
Adrees Muhammad: Yeah.


00:45:55

Chun Shao: Okay, because they are in the document revision. But when we enable the previous one, we also need to enable the first two document revision ID as from disabled to enabled. Okay. Otherwise all the four images will be showing like a deleted. Okay.
Adrees Muhammad: Okay.
Chun Shao: Because you Yeah. Yeah.
Adrees Muhammad: Yeah. In that case what we will do what I what I thought like uh in the case of sec if we delete the second execution what we will do is uh first of all we will disabled all the four
Chun Shao: So,
Adrees Muhammad: document revians we have in the document revian uh uh property. Okay, that's all and we will make that uh as uh deleted that execution. Then we need uh the previous as uh active. So we will make the previous one as active as well as I will check the document ids. What are the revian ids we have in the previous one. Then I will go that uh to those revisions and make those as active.


00:46:57

Chun Shao: Yeah. Not like a Yeah. Okay. What documents revisions need to be enabled is based on which execution is enabled.
Adrees Muhammad: Yeah. Correct.
Chun Shao: Yeah. Yeah.
Adrees Muhammad: Correct.
Chun Shao: So in this case we can we can keep everything on track.
Adrees Muhammad: Yeah.
Chun Shao: All right. Let's sort about another scenario like let's say a bank statement okay bank statement they have version one okay and they have a execution okay then they upload another document with another revision so and it as a another second execution and then we mark the second execution uh as uh disabled and reenable the first one uh so it will work because the second revision ID will be marked as disabled and based on the first execution it stores this first excusion uh revision ID then it will be reenabled. So when they check it even though they have two revisions but because the newer one has been disabled uh when they try to get the document it's still going to be the first uploaded version and this one is linked to the first uh execution.


00:48:12

Chun Shao: Yeah. So this will be no problem.
Adrees Muhammad: Yeah.
Chun Shao: Yeah. Okay. Good.
Adrees Muhammad: So and uh one more thing like uh we will uh where we will keep track of like which processor need uh one execution and which multiple. So we know bank statement needs multiple execution and driving license need one execution but uh is there any way to keep track of that.
Chun Shao: Mhm.
Jude Pineda: Uh I think we can just put it uh directly in the processor class itself. Maybe we could put like a a constant.
Adrees Muhammad: Okay.
Jude Pineda: It is a per document execution or a singular type of execution.
Chun Shao: Yeah, even hardcoded. I I mean I I didn't see a problem with that. Even hardcoded. Okay.
Adrees Muhammad: Okay.
Chun Shao: Yeah. If you want to save some like a Okay. If you want to save some like a code and you want to config it, I I totally agree with that. Yeah. Uh but I would say this this is not a big issue.


00:49:14

Chun Shao: Even hardcoded one will be okay. Not too bad. Okay. Yeah. Next.
Jude Pineda: I I just have to clarify first. uh address uh uh June uh is this document uh does this document here mean uh all type of documents I I mean let's say for bank uh for the driver's license is uh front and back for a owner one is it a single document record or is the front and back different document records
Adrees Muhammad: So yeah, can I answer that? Yeah. So from the document you can visualize it as a one input upload field in the front end. Okay, that's one document. Okay. And you can re-upload multiple times again to replace the previous one. You can replace the uh then again the previous one. It becomes revisions of that document. So for the front and back you will have let's say two uh upload input fields on the front end.
Chun Shao: Yeah.
Adrees Muhammad: So it will be two different documents. Okay.


00:50:25

Adrees Muhammad: So currently we have only one input field but you just visualize it as a two different input upload components on the front end.
Chun Shao: All right.
Adrees Muhammad: So on one component we just upload front end on second we will upload the back end. Okay, this time make sense.
Jude Pineda: Okay. Okay, I got it.
Chun Shao: Mhm. Oh yeah. Actually this way your design is much easier. Okay. You keep a current revision ID in the document. Okay. So you can easily switch like which revision you want. by change the revision current revision ID you can you can implement it yeah okay so uh so it's like a okay if in the front end they decided okay uh the second document I uploaded is wrong we should uh go back to the previous one so he just need to like click the previous one the first file uploaded and make it like a use this one. Okay, use this as the document. Use this file as the document.


00:51:33

Chun Shao: Okay, it will switch this revision ID and uh it will emit a popsup message of the document updated message to uh to to to Jude uh process module and it will rerun the aggregation. Uh right. Um yeah. So the aggregation need to check. Okay. Um because they set this revision uh like uh as uh as we enable this revision document revision ID again and it has a previous execution uh with this underwriting with this processor and with this document ID and also with this uh same uh revision ID. So instead of create a new execution, it will mark this execution as the most updated one. You understand what I'm talking about?
Jude Pineda: Uh, my internet got lost a bit. So,
Chun Shao: Let let me talk this. Okay, we have a bank statement and they uploaded one file and it has an execution. Everything looks fine and then they mistakenly upload a driver license override this document and it has a failed execution. Okay. So when the underwriter check find out oh I upload uh a wrong document to override the correct one.


00:53:19

Chun Shao: So when they click the document and it will see uh the history of this document that is the first one is a PDF file which is correct the second one is a image file which is not correct. So what he will do is he will check the first PDF file and say okay use this revision document revision instead of the image one image file. So it will change the revision and if you can switch to see the database in the database actually the document maintains a current revision ID there. Okay. Yeah, there remains this current revision ID. So what address will do is in the API module very simple is just update this uh current revision ID. All right. and emit a message pops message is updated and in this update it includes nothing else just underwriting ID and the document list and uh as bank statement and updated and with this document ID okay so what you will do is you receive this message okay and it's update this document and you find out the processor purchased And uh after all the filters it's just uh bank statement processor and which document is uh in this uh this document.


00:54:55

Chun Shao: Okay. And uh then uh what you will do is you will go to the execution list. Okay. Use the underwriting ID, processor ID, the document list harsh and the document revision ID. Okay. And use this for and you will find there is already okay a execution there with the same everything. Document list hash doesn't change. Document list revision uh ID doesn't change. Okay. So in this case instead of like a run uh new create a new execution you what you will do is like to mark this uh execution as the uh current en like enable it. Okay. So um yeah and uh disable the current one and uh then you you will you will not create a new execution but you reenabled the previous execution that is linked to this revision.
Jude Pineda: Okay. True. Yeah. Should it be like a different another flow here like say execution invalidation or should it be another section here?
Chun Shao: Yeah. Okay. Um let me think how to handle this.


00:56:36

Chun Shao: Uh at address part is better or at your part is better. update revision. Reision updated. Okay.
Gene Rellanos: Um I think we can let the API handle that because in the re uh revisions we we will not be dealing with any files with any new files right we'll just be re reval uh Yeah.
Chun Shao: Mhm. Yeah. So address or what's your opinion? Is that okay? All right. So you need to handle these two things. One is the document revision has been changed. Okay. revision ID has been changed. So what you need to do is not only you update this document revision current revision ID in the database. Okay, you also go to the execution data table and try to find out any execution that is linked to this uh documented revision ID if there is any. Okay. And if you find found any uh with the same underwriting ID, same process ID, same uh document uh list hash, same uh revision ID must be match all these criterias then uh you will check okay based on this uh uh this one you because it's already marked as the updated did.


00:58:50

Chun Shao: Next one is uh which execution and uh you will find out the next one all the way trace it to the last one which has the next update value is now chase it all the way down and uh mark it as like disabled. Okay. and uh uh reenable there's no enable like a uh set it as the first one as uh updated ids now okay and it will be reenabled uh and the last one will be disabled but it's not in the chain the first one is not in the chain anymore Four.
Jude Pineda: Uh so my so will uh aggregation follow after that?
Chun Shao: Excuse me. What?
Jude Pineda: So you said uh address will have to uh like look for look for all the executions relating to that uh specific document revision.
Chun Shao: Mhm.
Jude Pineda: uh uh so when will the aggregation be triggered uh like if there's instance because we have uh updated all the current like uh I mean executions
Chun Shao: Yeah. And then okay this all handled by the API level with the database and when you receive the okay when you receive the popsup message that is this revision of this document has been updated.


01:00:31

Chun Shao: Um okay you but you still need to check the database first whether there is any execution linked to this revision. If there is so don't need to create a execution you just uh run aggregation but if there is no execution link to this revision document you have you you you has to uh create a new execution. So it will be like a new execution a little bit complicated.
Adrees Muhammad: Yeah, I think it seems too much complicated. So, yeah. So, maybe we need to think about it to find another optimized approach. Uh
Chun Shao: Yeah. Yeah, because this is uh related to the revision of a document and uh what we need is to uh make it clear of the relationship among document revision and execution. Right? we need to maintain a clear relationship among these three uh records in the database.
Gene Rellanos: Yeah.
Chun Shao: So any one of them changed we can like a coordinate to make sure the most current uh execution and the document they are matched together. And also this last


01:02:32

Adrees Muhammad: Uh so like uh if we find out like this revision we need is the current revision we need to change it. So we will find out the execution against that. So if the multiple executions will have this revision and uh multiple execution is enabled as well.
Chun Shao: So, can you see that again?
Adrees Muhammad: So which execution we will go with like uh uh let's say user change the review of the document in front end so we need to reflect the execution as well in that scenario.
Chun Shao: Mhm.
Adrees Muhammad: So we will uh I will find out uh okay so which execution is linked with that revision. So I found multiple executions is linked with that execution. Okay. So in which the multiple executions are enabled. So which execution should I proceed with? That's Yeah.
Chun Shao: Yeah. Wow. It's too complicated.
Adrees Muhammad: So
Chun Shao: Okay. Okay. By instinct, I would tell you. Okay. Trace the link. find the like the last one which the updated ID is now.


01:03:51

Chun Shao: Okay, this is the most updated one and uh yeah. Okay, if revision change
Adrees Muhammad: But this one more thing this revision will depend upon the other documents revisions as well. What if the let's say we we found the uh uh we found the document revisions uh which which revision we are looking for but the other revision of that particular processor execution revision is uh disabled or deleted. So we need to check that part as well. Isn't the other revision in the document ids list are currently enabled or not? So there's a lot of things we need to
Chun Shao: All right. Okay. Mhm. Okay. So now let's make it clear eight execution. Okay. Now we have like a uh three different types of execution. The first is relate to the application fields doesn't involve any document. So we will not have any problem of like a revision. Okay. So we can ignore this one. And when we like uh focus on the execution part the enable one the disable one we just uh have operation on the execution and run rerun the aggregation again that's it okay so this is simple and the second one is like driver's license all right it's relate to document but it only maintain one execution so the execution is not linked to any document ID It's document ID free.


01:05:40

Chun Shao: Okay. Even though they keep all the information of revision ids everything but it's it's not like the execution is not linked to any ID. So uh let's say when they uh like enabled or disabled any revision uh and for these uh execution they will have a new combination of the revision ID for all the documents. Okay. And if there is any execution with the same ID and hash okay it will use the existing one because it's the same okay um and if there is uh anyone so you'll find that one and make it as the most current execution and if they cannot find it so uh the processor Well, create a new execution with this uh hash and uh revision ID combination. Okay. Um so um this is second. The third one is like a it's document related like a bank statement not only like a for the one processor it will have multiple execution available simultaneously. uh but based on the document ID. So each document ID should only maintain one active execution at a time.


01:07:22

Chun Shao: All right? Or make like a up to like a one most like uh available at one time. And in this case if there is a revision change uh we will similarly with the document ID and hash and the revision ids both we try to find execution and if it's there we will make it be the most current one and uh mark the rest under the name yeah document ID not only processor but also the document ID as disabled this will not affect other documents yeah so this operations it's it's like a uh way beyond this understanding of this uh API and the data module because it's particular uh processor related one. Okay.
Jude Pineda: Uh June uh address uh how about we make like a add a new table.
Chun Shao: Yeah.
Jude Pineda: Let's say uh let's say uh what what do we call this? Maybe like just active maybe you could say like active executions table uh where where we link the execution and the document revision inside it.
Chun Shao: Thank you.
Jude Pineda: And for each uh record uh the latest one should represent the the uh the active ex the active execution for that specific document or stipulation.


01:09:06

Chun Shao: Nice.
Jude Pineda: That way we have a we can trace what what previous uh executions have been uh maybe like disabled. We could just uh add new record to it and that that new record should represent the new uh the new active executions. Maybe more just like a timeline where the latest record of that specific execution or specific document revision represents the active execution.
Adrees Muhammad: Uh okay. Uh I have one more solution in my mind which may be more optimized. Let's say in document schema we have a stipulation type. Okay. We know we can have multiple documents objects but uh the stipulation type of all will be the same. Okay. Let's say in this form of driving license, we have two documents u for uh front or back. Okay, we have two documents but both the stipulation type is driving license. Okay, so what we can do is we can first of all find out the stipulation type which we are looking for against which we want to change the revision. Okay, enable or disable.


01:10:20

Adrees Muhammad: First of all, we find out the stipulation type. Okay, we find out the stipulation type. against the stipulation type we find out these are the documents we have against the stipulation type. Okay, good.
Chun Shao: Mhm.
Adrees Muhammad: So we have a latest revision property here as well. So we have the latest revision id as well for each of the document. So it becomes the array. Okay, so we have a array of document ids with the same stipulation ids. Okay, that's great.
Chun Shao: Mhm.
Adrees Muhammad: What we will do? We will calculate the hash. Okay, we have a hash. Now I will compare this hash with the hashes in the processor executions. If the hash match then the execution is this of that particular document. Did you understand? Yeah. Understand? So it will be I guess more efficient. It will not be that complicated. It will be simpler. So we just find out the stipulation types and for each stipulation uh let's say we have two documents again drivers.


01:11:20

Adrees Muhammad: So we have two docu uh document ids. Okay, we will hash those and uh we will have a document hash and in the processor execution we have document hash as well.
Chun Shao: Who?
Adrees Muhammad: We will compare those and we will find out. Yeah. So this is the execution which link to that to those two documents. Okay. So it's the current execution now. Problem solved. Yeah.
Chun Shao: Yes, that's a good idea. That is we only use Okay. Now we are not using documents but we use a stipulation ID.
Adrees Muhammad: No, no, no, no. Not the stipulation ID. Stipulation type. Uh Jude, can you go on top?
Chun Shao: Yeah. Type.
Adrees Muhammad: Yeah, we have a in the document we have a stipulation type property as well.
Chun Shao: Yeah. Yeah.
Adrees Muhammad: Yeah, on top.
Chun Shao: Yeah. Okay.
Adrees Muhammad: Yeah.
Chun Shao: So like uh for example for Javus license okay any execution. So in the now in the process execution we will keep okay we will keep uh a stipulation type there.


01:12:25

Chun Shao: Okay. To indicate uh like the stipulation type of this execution.
Adrees Muhammad: No, no, no.
Chun Shao: Mhm.
Adrees Muhammad: We don't need to keep that. Uh let me explain you again. Let's say we have a driving license. Okay. In that case we have two documents front and back. We will have two rows in that scenario. Okay. With uh but the both of them the stipulation type will be driving license. Okay.
Chun Shao: Mhm.
Adrees Muhammad: So now uh we process uh we perform the execution. Okay. In the execution, the document ids hash will be these two ids of these two documents. As we discussed previously, the document hash will be the ids of the document itself, not the document revision. Okay.
Chun Shao: Yeah.
Adrees Muhammad: So, we will have a document hash. Okay. So, it means these two documents are linked against that execution.
Chun Shao: I don't know.
Adrees Muhammad: Okay. That's fine. So what we will do is we have a stip when the user wants to enable or disable the a specific execution.


01:13:30

Adrees Muhammad: So we have the uh stipulation time currently on the front end. So the front end what the front end will do it will uh give us the stipulation type. Okay. So we will go to the document table. We will find out the documents against that stipulation type which will be the driving license. We will get get the two documents. Okay. uh and we have the ids of both as well. So we will just uh make an array and just hash that values. Okay. Now we have hash. So I will go to the document uh processor execution table. I will uh find out which processor execution h uh which processor executions document list hash match to that hash. So okay I will get the execution. So this will be the execution against these two document ids.
Chun Shao: Okay, good. So the hash is generated from the document ID or from the revision ID.
Adrees Muhammad: the document ID only, not the division ID.


01:14:29

Chun Shao: Okay. Uh my suggestion is let's do create this hash from revision ID.
Adrees Muhammad: No, no, it's uh it will become a problem. As we discussed previously, I want it as a review ID, but you said it should be document IDs and I thought the point and you you are uh correct. We should go with document ids and you Yeah.
Chun Shao: Yeah. Yeah. Yeah. Yeah. So because like now we we thought of this all roll back everything. I changed my idea. Okay. Can you give me five minutes? Let me explain my idea. But you you bring up a very good point.
Adrees Muhammad: Yeah. Yeah.
Chun Shao: Okay.
Adrees Muhammad: Yeah. Sure.
Chun Shao: Now uh the key to identify a execution now will be two things. One is the processor ID and the second will be the document hash. All right. Okay. So the processor ID uh when I talk about process ID I I talk about like the particular underwriting process ID.


01:15:34

Chun Shao: Okay. is not a processor key or not like a uh other things like this is a uh in this underwriting this processor has its particular ID plus the document hash as the primary key for a execution. Okay, these two compose this like okay now we have two situations one is we have updated document okay revision different revisions and we need to create a new execution. The second is we falsely rerun the execution. Now we need to separate these two executions a update of the document different revisions execution they will have different hash. So this could be able for us to roll back to any combination of the document of the revisions. Okay. But there are still another one that is even the hash are the same. The documents are the same. Revision are the same. We can still enforce to rerun the execution. So in this case, the second case, we will use this updated execution ID. All right? And this is a link. But for the previous we will keep multiple records.


01:17:12

Chun Shao: If the document revision hash has been changed there will be create execution. But if the hash is not changed and there is execution we'll use this execution and based on the link the updated execution ID we can find the most updated one. So we will not create a second uh execution with the same process ID and uh document revision hash. We will not. Okay. So and in order to do that we need to be similar as document and the document revision we need to maintain a processor uh current execution list. So for most processor it will only keep one execution as the most current result but for bank statements it will have a array okay to keep this uh uh keep this executions. All right so let let me talk about like a put aside of bank statement. Let's look at all the others. So all the others will in the in each processor in each uh underwriting processor it will keep a like the most updated or current execution only one. So what they will do is we will not maintain a link nothing there.


01:18:40

Chun Shao: We just have a list of all the executions. We can get it from the process execution with based on this uh process ID or we can have five six but there's only one that is marked as enabled. So it will be very simple for the API for the user interface they can market this execution as enabled or that execution as enabled. Okay. Um and while they mark this as enabled because this execution maintain a revision ID. Okay. Um list. So it will go to each revision find out its document and update the document current document revision ID with the this one to replace it. So um this change will be synchronized the execution changed the document revision will also change it's because the execution maintains the relationship with document revision ids okay this is one all right and on the other hand if they change document revision they said okay I want this document revision as the most current one you're changing the database with the document revision current one and in the execution table you use the hash to find is there anyone of this if yes you just mark that execution uh the current processor execution okay you replace the current one all right and uh that's it if there is no for this combination of the revision you just create another execution So this can handle all different kinds of information.


01:20:30

Chun Shao: Let's say if there is a driver's license and you have four documents uploaded and each document you upload another file. So for each document you have two versions. Okay. And how many different combinations of revision you will have is two to four. That will be 16 different combinations of revisions. Okay. So this could be very complicated but even that complicated because we only focus on the revision ID combination the hash. So no matter what kind of revision you want to change it's simple you just find out the execution link to this revision combination and make it as the most current execution. That's it. Very simple. Okay. So far are you clear? So any question? We haven't talked about the bank statement but I want to make sure so far I make me I make myself uh very clear to you that the processor execution have two primary key besides its own ID have two primary keys combination to determine one execution is the processor ID and the document revision hash this one or this one.


01:21:59

Chun Shao: Okay, if there is duplicated, it's use this updated execution ID. Okay, this update execution ID link this chain will only used with the force execution rerun. Even you have the same hash code, rerun it. What's this? Any question? Oh, you get lost. If you get lost, you also let me know. Oh, everything.
Adrees Muhammad: Yeah, bit closed.
Chun Shao: Okay. Yeah. Okay. I I will explain that again. Okay. So, the purpose of this design is Okay. Trying to handle all different kinds of combinations of document revision because this document revision is very complicated. So to handle it simple, it's like we have a fingerprint of the document combination of document revisions. I use this Java license as example. Okay. Sometimes you have two images and you have a two document revision ID. Sometimes you uploaded two more then you have four document revision ID and sometimes you override the two then you have like a uh another combination of document revision ID.


01:23:36

Chun Shao: Okay. And each time you do some update there will be a uh related execution there. What we want to do is we want to find the mapping between the execution and the combination of revisions. Okay? Because no matter you overwrite a file or upload a do new document or remove the document, the document ID didn't provide enough information to track all the changes. But the document revision ID can provide this kind of changes for this part. You clear?
Adrees Muhammad: Yeah, one thing like uh in the case of let's say driving license, we have two documents front and back. It will not be two revisions. It will be two documents. Each document will have one revision.
Chun Shao: Yes. So it's like a list of document revisions.
Adrees Muhammad: Yeah.
Chun Shao: Yeah.
Adrees Muhammad: Yeah.
Chun Shao: And we will hash the whole like if two revision ID then we will hash two revision ID. If this time they upload two more then becomes four revision ids. We hash the four revision ids and the next time he upload another two to override the previous two.


01:25:02

Chun Shao: Even though we still have four revision ID but two revision ID has been changed. So it's a new combination of revision ids and a new hash code.
Adrees Muhammad: Yeah, correct.
Chun Shao: Okay. So in this case we handle we cover all different kind of combinations all different kind of changes they could make on a document. Right?
Adrees Muhammad: Yeah.
Chun Shao: Yeah. So in this case okay uh we can keep track of the change of this uh document revision and the execution. Okay. So any change of the revision of the document uh uh on the on the document side what Jude will do is not always create but use the document revision to check whether there is already a execution. Okay. and uh if there is okay use this execution to update the processor. So for the underwriting processor it's similar to a document okay you will maintain a current execution list and for most processor it will be only one okay you can only keep one current execution and it's based on the com different combinations of documents Right.


01:26:42

Jude Pineda: Yeah. Yeah, that makes sense.
Chun Shao: Okay. All right. So it makes sense, right? So if I for example if this processor have four different executions no matter which execution I switch to I want to use this one I want to use that one because this execution we maintain the hash of the
Jude Pineda: Yeah.
Chun Shao: document revision ID and also the list of document revision ID and we can use this revision ID and to update their documents to this ids so we keep synchronized no matter which execution you switch to, you will have that uh document to be the correct revision according to this execution. Correct? Yeah. Yeah. Yeah. And similarly no matter what document revision you want to change, you want to switch, you want to upload, you want to delete. If there is already execution there, you just switch to that execution. That's simple. That's it. If there is no, you create a new execution and set the new execution as the most current one.


01:27:56

Chun Shao: Okay. So in this case we cover the situation of B of Java license that is this processor is using documents okay but like uh is using documents and the documents could be very complicated but it's only maintain one current execution most current execution okay so if you are clear about this I will then talk about the bank statement. What are we going to do with the bank statement? It's very similar. Okay. So far you good?
Adrees Muhammad: Yeah.
Chun Shao: Okay. All right. Now uh for the bank statement bank similarly it will have a harsh for the revision. Okay. So let's say if they have a bank statement uploaded and we process this bank statement and we have a execution. This is in the beginning and then they upload another file override the bank statement because we changed the revision ID changed the hash changed it will create another execution okay it's not like we update this uh update execution ID this link no no no it's not like that we keep like a a list of executions but we update the most current execution for this processor and we put that into the list and we will replace the previous one and when we want to replace it at this time we will keep make sure that the document ID okay the execution has the document ID which are the same so if the document ID not same then


01:29:50

Chun Shao: we will create a new execution there Yeah. Yeah. Yeah. Yeah. You understand what I'm talking about? So let's say in instead of like a overwrite you upload a document that is actually another document okay and it has different revision ID and you create a execution and then you decided okay I will put this new execution into the most current execution of bank statement processor and uh for the bank statement processor to handle this it's not just like oh I override the previous one. It will check the execution's document ID and see if there is any exurren execution in the list has the same document ID. If it has the same, it will remove the the one and put a new one. If there's no the same, it will just add a new one. So, it will become two executions in the list instead of one execution in the list. This is if they upload a new uh bank statement document. Okay, if they don't upload, it's just an overwrite, it will override also the execution in the current execution list.


01:31:11

Chun Shao: And if they want to forcely rerun the bank statement processor, okay, forcally rerun the documents revision ID are the same. So this is the time we use this updated execution ID and it will be a link. Are you with me? I'm explaining when we are using this updated execution ID, it's only happened when they share the same process ID and the same hash code, same document revision hash.
Adrees Muhammad: Yeah.
Jude Pineda: I think I think I'm confused now. Just
Chun Shao: Yeah. Yeah. Yeah. Okay. All right. Now, let's go back to the first one that is there is no document, just a processor. Okay. And uh because you don't have document, you don't have document hash. Okay. So there will be multiple executions if like you change keep change for example the yin number you have one number there's execution you update the y number the second execution. Okay. And then when you say okay I will update I I I will change the execution to the previous one because you don't have this document ids uh revisions so they will switch back to the current to the execution but for now we don't have a way to roll back to the previous EIN number.


01:32:57

Chun Shao: Would this be a problem? Do you think this could be a problem or you think this is not a problem or like uh uh Jud told me that oh actually we do save the EIN number history and we can roll over back. Judas me.
Jude Pineda: So for the AIN uh we don't have records of like previous values right
Chun Shao: Yeah. So it's like a when you create a execution uh for example it's like a clear business report and we use the name of the business DBA and the EIN probably I guess this these are the three uh like a fields uh data we care about and use it to get the get the uh report right okay yeah and let's say Okay, they accidentally delete the EIN number and because we because you received
Jude Pineda: Yeah. And some more.
Chun Shao: okay this uh pops up message so you run a new execution and uh because you only have the name you don't have EI number so the clear report give you a error result you didn't get anything and this execution well be nothing and the all the previous were gone and then you say, "Ah, I made a mistake. I


01:34:38

Chun Shao: delete the EIN accidentally." So you said, "I roll over." Okay, I I have two execions for clear and the previous one I want to enable it. So you can go ahead and enable it. No problem. And all the factors pre-check will follow the steps because you reenable the first execution. And because it's no document related, so we don't need to uh worry about the document change. But let me ask you first, do we need to roll back to the information like when we run the first execution? The second in current design are we available to do that?
Jude Pineda: I don't think there's an available way to roll back uh application form or tune because Unlike document revision, we have uh we have like a record of the changes of that specific document. But for uh specific fields of the underwriting, I don't think there's any
Chun Shao: Mhm. So that means okay they can roll okay if it's not document based they can roll back to that execution but we will not update the application data.


01:35:54

Chun Shao: We will not roll back it. Can you set up these?
Jude Pineda: Uh, I thought you said that the execution was triggered because of the updates from deleting the EIN.
Gene Rellanos: Hey.
Chun Shao: Yes. Yeah. Adris, what's what's your
Adrees Muhammad: Yeah, in case of EIN, so we have a factor table. So here we can use the factor table. So in the factor table, we we have a record of the previous EIN and in the factor table we have the execution ID as well. So from that we can go back through that execution.
Chun Shao: Uh no the factor is the result and the ein is the input okay.
Adrees Muhammad: Okay. Okay.
Chun Shao: Yeah. So like a ein is the uh tax ID and uh the factory usually will store something like um like is this like a bankruptcy?
Jude Pineda: Yes.
Chun Shao: Okay. like this uh this uh this company is it bankrupted something like that. So it's different. Yeah.
Jude Pineda: So yes J uh unless we have like a record of changes stored in the database we can do roll backs but in this case we only have like a flat data here a single row like there's like no


01:37:07

Adrees Muhammad: Okay.
Chun Shao: Mhm. Okay. Uh yeah.
Jude Pineda: tracing so I think roll back is uh is impossible for this now for this right
Chun Shao: Mhm. Okay.
Gene Rellanos: But we can roll back the the result right or the the execution just not the the EIN. So the Aen is lost but the execution we can roll back.
Jude Pineda: Yes.
Chun Shao: Yeah, we can roll back the execution which is uh like a at least for like at the next step processing business check. No problem. Yeah, it's just the previous CIN is is accidentally deleted.
Gene Rellanos: It's lost.
Chun Shao: Okay.
Gene Rellanos: Yeah.
Chun Shao: Yeah. Okay. And we are talking some like like very extreme case. So far I I'm already uh like a satisfied with the solution.
Gene Rellanos: Ethics.
Chun Shao: I don't know whether now you are with me. You're clear of like what we design. So the updated uh execution ID will only be used with like the force execute. If it's not force execute, you will like find whether they have the same uh execution in there.


01:38:41

Chun Shao: And if it's application data uh no it's there is any change you will run the execution but for uh processes as is related document you need to find the revision ID hash and compare it and find out okay if there is one you will enable that execution instead of create a new one okay but it always can like for one execution You can rerun it forcely rerun it.
Jude Pineda: Yeah, I can understand the G tune but not really like the total uh technicality.
Chun Shao: So yeah. Yeah. Okay. So we need to change the database a little bit. Not that many. Okay. But we need to change a little bit. So for uh like a can you scroll down to like underwriting processor? Yeah. So here we need to put a like a current execution list. It's like a just like a document. Okay. Current execution list. Yeah. And it stores all the most current execution ID. Okay. It's an array ID array.


01:40:12

Jude Pineda: Uh, is already hit the correct syntax here?
Chun Shao: Yeah. Yeah. You can you can change it later. Okay.
Jude Pineda: Okay, got it.
Chun Shao: And next in process execution. Um yeah, scroll down. Process execution. Yes. So for the processor execution um this uh document list hash you need to change it okay to like a no uh you going to keep the name but like a strong hash of document revision ids instead of ID. Yeah. Okay. And I think yeah that's it. And keep in mind the updated execution ID only used when there is a force execute because they share the same okay uh same ID.
Adrees Muhammad: Okay. Uh in the case of force execution, we will not create another execution. We just use the previous one or we will create the new execution.
Chun Shao: Well, I create a new exusion.
Adrees Muhammad: Okay.
Chun Shao: Yeah.
Adrees Muhammad: And uh okay.
Chun Shao: And then this case they they uh maintain a link from here.


01:41:34

Chun Shao: Yeah.
Adrees Muhammad: And uh regarding the property in uh underwriting execution uh you mentioned we will save the means the most upgrade executions. So which execution we will save like uh this table underwriting processor is basically uh it will uh be an processor with that underwriting. So uh which execution we will save like can you explain that?
Chun Shao: Okay. So like whenever there is a new execution uh for most of the processes okay when there is a new execution this will be replaced by the new execution whenever there is created so doesn't matter the result is failed or is succeed once a new execution for this processor created you replace it with this one the only exception is for bank statement processor So the bank statement processor will maintain actually a list. Okay. And uh it's based on the document ID not document revision ID. It will based on document ID. Okay. If there is two documents will be two executions here. If there is three documents will be three docu executions here.


01:42:56

Chun Shao: and any replace well not only like uh based on the process ID but also the document ID.
Adrees Muhammad: Okay, that carton.
Chun Shao: Mhm. Yeah. Okay. All right. Yeah.
Adrees Muhammad: Chun I have mentioned one thing isn't the meeting is recorded like uh phantom is not there we discussed a lot and it's unfortunate.
Chun Shao: Oh yeah. Why the phenom is not there? Oh, okay.
Adrees Muhammad: Yeah.
Chun Shao: I only get uh Gemini like help help us to write the summary. Okay, at least we have something but it's not recorded. Uh that but uh I mean we didn't change a lot. Okay, the design of the schema database schema we didn't change a lot. It's just the workflow.
Adrees Muhammad: Yeah.
Chun Shao: Yeah. Okay.
Gene Rellanos: Yeah, the workflow to handle the revisions.
Chun Shao: Yes. So like uh if we if you scroll up uh from the popsup messages now you will see we have updated we have created and we have execute and yes execute will be a very different workflow.


01:44:47

Chun Shao: uh you you can separate it up and we also have like a uh on like a underwriting processor.execution dot like a uh how do you say update? So we update which like a uh like a execution is the most current one. So this will trigger uh new workflow and similarly we have another one which is um the underwriting and uh document. Uh no no that's included in the in the in the update of the of the message under writing update. Yeah. Any change on revision will be on the document update. Yeah. Yeah.
Jude Pineda: What is this label correction?
Chun Shao: Yeah. Something like that. And this will be emitted by address in the API uh of uh the execution. So they can set up one execution as the most current one to replace the other the others.
Jude Pineda: Okay. So,
Chun Shao: Yeah. because they updated it as most current one and when you do the aggregation you will go to this processor and find out the list of current execution and use this executions uh like intermediate result to do the aggregation.


01:46:29

Chun Shao: Yeah, since we maintain this that will be much more easier. Okay, there is one thing I haven't mentioned is if okay if there is an execution that is force wrong okay force executed so it's in a chain so this execution has like a a updated ID okay and it's marked as okay I want to use this one instead of the other one. So let's say this is scenario. We have a bank statement and it run once. Okay. And we didn't change anything. We just want to reforce it to execute again. Okay. The previous execution we have a result uh and we have an execution. And then when we run rerun it again it will have the second execution and the first one it will be updated as the update execution ID will be the second execution. All right then okay the underwriter looks at the second execution and find out the result is even worse than the first one. So he want to use the first instead of the second.


01:47:56

Chun Shao: What will what should we do instead of like uh we also need to update the processor uh current execution list? We need to update over there. Should we also do something in the link? No, we don't need to do anything in the link in the chat. Oh, it just highlight the first one as even though the second one is running after the first one, but the first one is the one we picked. Yeah, we don't need to run uh we don't need to change anything on the link. We just keep the link as is. Once it's established, it's established. We not change the link, right? Are you with me? Yeah.
Adrees Muhammad: uh like if you if you want to get the latest execution if we don't change the link now the latest execution is uh like the first one. So how we will get that if we don't change it But
Chun Shao: Yeah. Yeah. Because because now we get the latest execution from the uh from the underwriting processor table.


01:49:12

Chun Shao: They have a field called current processor list. We get it from there but not get it from the link. contract.
Adrees Muhammad: if we if we change the link, will it break something?
Chun Shao: No, we will we will not it's not necessary to change the link. We just keep the link as is. It's just a record to trace the uh like the steps of this uh the relationship between these executions.
Adrees Muhammad: Okay.
Chun Shao: Yeah. Okay. So let's say this okay for one processor if we change the revision and the executions will be separate so it will be like this one and the two okay like this way but if there is a reforce uh like a forcely execution nothing change but we just forcely run it because there's a link so in the UI it will not be separated it too but it will be a little bit overwrite. Okay, it will be a little bit overwrite and usually it's this one will be like the most updated one will be selected as the current execution but we can switch.


01:50:33

Chun Shao: So it will be like this. This one the older execution will be appointed as the current one. And the only thing we need to change in the database in the database is the list the current execution list for the link we don't need to change any link and because we have a link so in the UI in the front end we can put these two connected together they know that there is a forcely run but if it's not forcely run it's because we change the data it will be separated.
Jude Pineda: um by LinkedIn. Uh what do you guys mean by that?
Chun Shao: Uh what can you say your question again?
Jude Pineda: Uh the word link, uh what do you mean by that in this context? Uh uh yeah, you you use the word link.
Chun Shao: By what link?
Jude Pineda: Uh I'm sorry, I got confused.
Chun Shao: Yeah. Yeah. Yeah. Yeah. Okay. Let's say we have a processor in the front end. Okay, UI. We have a processor and we need to list all the executions.


01:51:41

Chun Shao: Let's say it has a five or six different executions. Okay, if the document revision ID changed. So this execution is executed because of the change of the document. Then they are separated when you present it in the front end. They are separated. That means they are not uh their data source are different. Okay. So they they are separate executions and when you when you try to forcely rerun like a okay for this execution okay we have this uh uh document ID okay revision ID and uh you can write click on it and uh rerun it forcely rerun it. So the new execution will not be separate present in the front end actually will be a little bit overwrite to indicate these two executions share the same hash code.
Jude Pineda: Oh, okay.
Chun Shao: Okay they share the same hash code it's rerun and it's linked. Okay so in this case um yeah we can we can have information. Oh okay. Now uh I would say um Jude please say even it's not document related.


01:53:07

Chun Shao: Okay. If this process is not document related it's based on the application data can you also save the application data as the payload in your exe?
Jude Pineda: execution.
Chun Shao: Yeah your execution.
Jude Pineda: Okay. Uh so I think we can add the payload here.
Chun Shao: Yeah. So in this case so we can re Yeah. Okay. So can we like a Okay. Can we combine the can we put the document list the revision ID also into the payload. So this payload will either save the uh like it's a JSON formatted. So you Yeah.
Jude Pineda: So I think it should store this Yeah.
Chun Shao: Yeah. Yeah. Exactly. Yes. Exactly. And we just uh hash the payload. How is that? We hash the payload. Yeah.
Jude Pineda: Uh for what?
Chun Shao: Yeah. The hash previously is only for document. If there's a document, we hash it. Right. We didn't hash the Okay.


01:54:21

Chun Shao: Now we just hash the payload.
Jude Pineda: Oh, okay. Okay. I get it. Yeah.
Chun Shao: Yeah.
Jude Pineda: Uh how about we just add it as a separate uh attribute during uh in saving tune like maybe this is for the actual payload uh in when we store it. Maybe we could just add like a hash here for example. Uh how should that work?
Chun Shao: No, the the the hash is independent to the payload.
Jude Pineda: Okay.
Chun Shao: Okay.
Jude Pineda: Okay.
Chun Shao: And then here when you provide this ID, remember uh in in your Okay. Can you switch back to the previous like examples? Yeah. So here should not be the document ID. You should include the u revision ID.
Jude Pineda: Oh, for each for each
Chun Shao: Yeah, because we hash. We're going to hash it, right? Uh, no, no, no, no, no, no, no, no, no, no, no. Okay, hold on one second. Yeah, so this is the payload you received.


01:55:25

Chun Shao: Okay. And when it comes to a particular processor, you cannot just hash the whole payload. you need to pick up the the items that this processor needed and hash it. For example, you you got this uh create created payload. Okay. And for bank statement, the payload is only the bank statement. Okay. The the ids, okay, you you need to hash it as the payload. Okay. You don't need to hash the other things because otherwise it's going to create a different hash code and you will not find the correct one.
Jude Pineda: Oh yeah, yeah, yeah, that makes sense.
Chun Shao: Yeah. Okay. And uh if there is any like uh for example um uh the the clear report business report processor you will not include the document ID into the payload. you will only include the merchant name ein these two in the payload as the hash. Okay.
Jude Pineda: This
Chun Shao: Yeah. So you need to like uh pre-process the payload and for different processor you just extract the data is interested and uh put that in the payload.


01:56:52

Chun Shao: Okay. So this payload will be different and the hash hash of the payload is based on the value of the payload. And in this case then we can roll back or we can give the option ask the user okay I have this uh you want to use this execution result and the application yin is different from the current one. So do you want to also reverse to uh roll back to the payload we save in this execution and update the application form data. Right now we we make it all covered.
Jude Pineda: Oh yeah.
Gene Rellanos: I see. So, so using the payload we can re re uh reinput the lost maybe EIN something. Let's say if the EIN is erased using the payload saved, we can write it back.
Chun Shao: Yeah, we can find it back. Yes, because it's saved in the first execution payload. We have the information, right? And uh if they want to roll back to the first execution, we have the payload and we can update at least those fields.


01:58:09

Gene Rellanos: Yeah. Yeah.
Chun Shao: Okay. It's similar idea with the document. Adris, are you with me? Yeah. So instead of use document list and document h I I combine it. you still can find the document list the revision ID inside the payload and the hash is on the payload. So it's not only for the document related processor, it's for all processor. Even there is no document, as long as they have a payload, they will have a hash.
Adrees Muhammad: So the payload will be uh this complete object right this one which Jude is showing.
Chun Shao: create object.
Jude Pineda: this way.
Adrees Muhammad: Yeah.
Chun Shao: Yeah. Yeah. Part will be part of this object.
Adrees Muhammad: Okay. Yeah.
Chun Shao: Yeah.
Jude Pineda: Ah so not totally this whole objection.
Gene Rellanos: Like the just the triggers that the triggers don't match for the processor.
Chun Shao: Not do though. Just the part.
Jude Pineda: Okay.
Chun Shao: Just the Yeah, just Yeah. Just the triggers.


01:59:12

Chun Shao: Yeah. Just the triggers they like they they care about. And uh Okay. Notice that if it's document related, you don't you even don't need like a create it or delete it or something. Okay. For the document, it's different story. All right. You need to get the revision ID and uh and get it. Okay. So this is this is when during the implementation you need to pay attention to. All right. For example, if they if they upload like a JavaScript, but when you generate a payload for the Java license processor, you should include all the most current revision documents instead of only include these two ID You should have all the ids. So yeah, this is this is uh this is one important thing.
Adrees Muhammad: Not just the updated one but the uh all.
Chun Shao: Yeah. But or Yeah. So pro.
Adrees Muhammad: So how Jude will identify on which pro uh I need to perform the processor.
Chun Shao: Okay. So maybe for each processor you need to define a function and this function is uh like a pre like a um create execution.


02:00:55

Jude Pineda: are
Chun Shao: Okay. So this processor will create execution based on this uh whole payload. You use it as the input parameter and uh the function of the processor will first check okay the triggers is actually whether the triggers is in this payload. If it's in it will be triggered. If it's not in it will return a now or empty array back. All right. This is first step. The second step is if it's triggered okay it will create a payload for itself. So based on the parameter based on the payload in the popups message it will create its own payload eliminate all the other things only keep the data for example if uh Javus license it will uh okay find out okay there is a stipulation called Javus license I I don't care what kind of a document ID saved it there I just go to the database find all the uh st all the driver license stipulation under this underwriting their most current revision and compose the payload and generate a payload hash.


02:02:17

Chun Shao: Okay. And use this hash to check if there is anything in the database already have this one. If yes, they will also return a empty execution list because it's already there. I don't need to execute it. Okay. And uh uh what I will do is uh okay yeah let's say this it well it will return the execution ID but this execution is already there okay it's created so you will return the execution ID all right and if it's not there it will create a new execution and return but the difference is the the previous execution the status is completed successfully and the Second status of the execution is pending. Okay, it's not executed yet. All right. And then no matter it's uh existed or it's not executed again, uh you will get a list of execution and then when you run this execution, okay, you will check the status of the execution. If it's completed or it's running or it's completed or even failed, you will not execute it. you only execute those that need to be executed.


02:03:39

Chun Shao: Okay. All right. And then uh after that uh you will get a processor list. So um the processor list will be the processor return a non empty execution list. Even though there is like a uh a execution that is already existed and completed previously but because you change you might change the execution anything so this will be this process will be included in the aggregation because you change the most current execution. Okay, let's talk talk back. Okay, come back to um the handling of this generate execution list. So if a processor received the payload and uh it finds okay there is no execution according to this hash code then it will create execution and uh then that's it. But if they do find a execution okay with this hash code they will also return this execution ID okay but at the same time it what it will do it will put this execution ID to the processor's current execution list use this to replace the previous one. So after the execution finished when they do the aggregation for this processor they will get the most updated information to generate factors.


02:05:24

Gene Rellanos: I see. So it's a kind of like a lookup when there's no uh when there's already an execution, it will look for the past executions as a as a source to make refactors.
Chun Shao: Yeah.
Gene Rellanos: All right.
Chun Shao: So what it will do it will update the current execution list in the processor. So when they do the aggregation they just search for those current execution in the array to do the aggregation. Okay. Yeah. In this case it's like a relatively simple aggregation. I only look at for this processor for this current execution. Okay. And uh for the oxure I only like I pass the payload to each processor and each processor you give me a list of execution list. That's it. And for the execution part you just run the execution only if it's pending. If it's already finished, you don't need to run it. Okay. And uh for the aggregation, you just uh run the processor uh which has eight execution. If it's return empty, that means you don't need to do the aggregation.


02:06:47

Chun Shao: Okay. So each step each process is independent and defined very clear of what it should do and what it should care. Okay. So I give you an extreme case. All right. Um so you have a uh processor and you create an execution and it's running. All right. and not finish it and then you mistakenly hit forcly rerun it. Okay. Uh or like you you you you changed anything and uh Okay. Let's use this as example. Okay. You enter the EIN number of a merchant and it start to run a clear report and you mistakally delete it and save it and then it create another wrong. Okay, create another wrong because the payload hash is different and then you find oh I go back and change it back. I put the same number into it. you changes the third time. Okay. And the third time it the whole process what what it will do it will use the payload and find out there is a execution already and it will return that execution and that execution returned with the status is not pending.


02:08:18

Chun Shao: It's already run. So it will not create okay it will not create a new like a how to say that a new a new execution.
Gene Rellanos: a new API request.
Chun Shao: Yeah it will it yeah it will wait for this execution status as like a completed and then it will like a to uh how do you say to the aggregation part. So even though it changed a couple times and because the value doesn't change it will not create a lot of execution unnecessary and they say ah each time I it will cost me $1 and you should refund me. We can solve a lot of problems like this.
Gene Rellanos: Yeah. Yeah. You can lessen the cost of the API calls.
Chun Shao: Mhm. Yeah. We can eliminate like reduce the amount of unnecessary execution if we use this uh payload hash code. Okay.
Jude Pineda: So uh you mentioned that yeah if the execution list is empty uh we don't need to run aggregation. Did I get that right?
Chun Shao: Yeah.


02:09:32

Chun Shao: If the processor return a empty execution list, we will not include in the aggregation. Okay.
Jude Pineda: But if if there's a deletion ch uh there would be empty executions list because we have like deletion right?
Chun Shao: If Uh deletion of what the document right?
Jude Pineda: Yes.
Chun Shao: Okay. Yeah.
Jude Pineda: But we need to aggregate the result so we can uh update the factors like after deletion like we only get the active uh executions or its factors so that we aggregate that results to get an updated data based
Chun Shao: This is Mhm.
Jude Pineda: on the based on the nondded uh execution document.
Chun Shao: Yeah. Um if it's deletion similarly it will return non empty execution list it just return the previous the current execution but because it's already updated so it will not run but it will indicate that to do this uh aggregation is that Okay.
Jude Pineda: Oh, so you so you mentioned uh executions list here uh is not necessarily to be executed.
Chun Shao: Yeah, it could be a finished execution in the list it returned.


02:11:01

Jude Pineda: Oh, okay. Okay.
Chun Shao: Yeah. So the processor will use the payload to find out it's the the data it's interested and make a hash and find out if there is any execution with the same hash it will use this execution otherwise it will create okay this is the how to handle the payload but if it's like a force executed it's another story. So that's what I say you need to create a different workflow for force execution then it it will not check the payload okay it will just rerun based on the same payload okay so when you want to re
Jude Pineda: Okay. Okay.
Chun Shao: like a force run uh pretty much it's gives you a like a execution ID and from that execution ID you will get the payload. Okay, same payload and you use this payload to create a execution and uh run it. Okay, so the execution were based on this payload, the same payload. Yeah, it's not complete.
Jude Pineda: So, do I have to So, do I have to update this too?


02:12:22

Jude Pineda: Uh, okay.
Chun Shao: Yeah. Yeah. Put in a separate workflow. It Yeah, it should have a separate workflow. Okay. Yeah. Okay. And uh you should have three workflows. Okay. But I'll show the first is uh underwriting created updated. This two will be one workflow. And the second is underwriting processor execute. This is second workflow. Okay. The second workflow will be much easier simpler. Zen. Okay. The third one will be uh underwriting processor execution update. So that is the update like which execution I want to use. This is a totally different workflow. So basically it's just a run aggregation for this uh processor. That's it. It's just a run aggregation. Okay. The second workflow, the processor execute the force execute of processor. You will create a new execution with the same process ID, same payload, same payload load hash, but different execution and you run it and you aggregate it.


02:13:41

Chun Shao: All right? And the first two update created even if it's deletion, no problem. Okay? after you delete it uh like a deleted document you will have a new hash and based on the new hash as long as you have the same hash you return the ID of the hash and uh if you don't have this hash for the payload you create a new one okay so it's like Um let's say if you upload a document to driver license then you create a new execution and then if you delete that document okay it will go to the database and find out okay there is no document and uh the payload will be empty. So for empty also we have a uh no for empty we we cannot create a new execution because it's empty right?
Jude Pineda: Yes.
Chun Shao: Yeah. So um so for empty you you will have to like a mark the processor the current execution to be empty and you will include the execution ID in your return. Okay. So in this case this will still be aggregated.


02:15:19

Chun Shao: All right. It won't uh won't affect the following process. So in this case we can handle this uh and we don't need to create another workflow to handle this deletion situation. Okay. But if it's only delete one document uh okay well it will be a little bit diff different for the bank statements because bank statements is relate to a document. So you need to pro uh handle it differently. But uh basically for Ouxure it will okay the workflow will be very clear. Okay get all purchase processors. Okay and for and for purchase processors filter out those disabled filter out those that are not automatic running. Okay. And you get maybe five or six list of processor and uh use the payload you received from the pops message to as the parameter to each processor and get a list of execution. Okay. And if list is Yeah.
Jude Pineda: So, so Here in processors list uh it should also return the previous executions list. Did I understand that correctly?


02:16:43

Chun Shao: Yeah, it's based on the execution list it's returned. If it's not empty, it will be including processor list. If it's empty, then you will not do the aggregation. Okay? Or it's like a you even don't need to mention this processor list. It's just like a okay for each processor you will get a execution list and then next step is to use threads to run the execution simultaneously and the next step is if the execution list is not empty you do the aggregation. Okay. But well yeah because it's all priorly so it's better to maintain a processor list because you need to wait until all the um completion of the uh executions to do the aggregation.
Jude Pineda: Yeah, I have to know uh what what executions that needs to be wait before the aggregation can be run.
Chun Shao: Okay. Yeah. Okay. Yeah. Okay. So now let me ask you a question. If a processor Okay. If a execution returned is pending, no problem.


02:18:09

Chun Shao: You start a new thread to run it and uh and wait until it's finished, right? It's no problem. What if uh the the execution is completed doesn't matter failed or like a like a other state or successfully and you you don't need to wait it because it's already completed and you can do the aggregation as long as the other execution completed also no problem. Now let's think about it. What if a execution one of the execution is wrongly?
Jude Pineda: So if one of them is running J tune I guess I'll have just to return that uh running instance because it's it's just processing the same documents list or stipulation data.
Chun Shao: So when there is one execution is running that means there is another like a processor like a this uh checking is waiting for the completion of that running right.
Jude Pineda: Uh yes yes June as long as it's using the same documents or stipulation we should just return that uh instance
Chun Shao: Yeah. Mhm. So after the completion of that execution running because it's in another thread it's not in this this running okay it's not in this one it's in another thread and we have no way to get oh is that possible to get a thread ID uh but after that thread running it will do the aggregation anyway Right.


02:20:03

Jude Pineda: Uh we'll just have to check the database record if it's running or not.
Chun Shao: Mhm. Okay. So, we make it simple. If it's running, okay, if the payload hash we get and we find out there is execution the status is running, we will not return it. We will not do the aggregation for this processor. It's because it is running. That means it will be another aggregation will be performed after that running ended. It's already there. It's not executed yet.
Jude Pineda: Oh, okay. So, we should uh exclude it.
Chun Shao: Yeah, we it will return empty.
Jude Pineda: Okay. Okay. Okay.
Chun Shao: So the only thing it will return is if there is a execution and it is completed either like a field or succeed it's completed you include in the execution list return to uh return to the orure. Okay, if it's pending uh or it is running that means this is already created by another uh thread. So you don't need to worry about that.


02:21:24

Chun Shao: That thread will take care of the aggregation. You don't need to take care you don't need to rerun it. So keep it empty. Yeah.
Jude Pineda: Okay.
Chun Shao: Okay. Yeah.
Jude Pineda: So for pending and running we exclude it for the specific workflow and for fail and completed we do a new execution.
Chun Shao: Yeah. Yes. Yeah.
Jude Pineda: Okay.
Chun Shao: Okay. Okay. So, rewrite.
Gene Rellanos: for the I have a I have a question for for the pending and running instance of an a processor in what scenario does that happen like maybe another underwriter performed this processor so so that it's running outside another
Chun Shao: Yeah. Ch. Yeah.
Gene Rellanos: thread your thread
Chun Shao: uh I can I can give you an example. So let's say we have a underwriting created okay and there is a processor and uh okay and it is like u uh how to say this processor is marked as okay uh okay let's say this okay we have underwriting and there's a processor and this processor execution will take a long time maybe like a five minutes to finish.


02:22:38

Gene Rellanos: I see. I see.
Chun Shao: Yeah. And then during this five minutes you changed it and changed it back. Okay. And you make a lot of changes and it will send a lot of like pops messages and you don't want like to create too many you know uh instance instance of the this execution. Okay.
Gene Rellanos: That's easy. Thank you.
Chun Shao: Mhm.
Jude Pineda: Uh, okay.
Chun Shao: Yeah. Yeah. No, I have Yeah, there is.
Adrees Muhammad: Like I have a question like if the processor isn't uh running so should we allow to update anything in front end I because we shouldn't allow user to update anything while it's in running. had to build the Yeah.
Chun Shao: Well, it's asynchronized. Okay. They upload the documents and create it and it will automatically running and at the meantime they can like a uh switch back to the list and click the details, refresh, check the status, make updates, anything they can do. Yeah.
Adrees Muhammad: Yeah, it's asynchronous but uh it's still in running states.


02:24:00

Adrees Muhammad: So if uh we shouldn't allow user to do it then we can make it a bit simple because uh instead of handling that part as well.
Chun Shao: Yeah.
Adrees Muhammad: What you think like because what a process is in running state uh so it doesn't make sense to maybe update uh something related to that process because it's already in running state. If we complete that then we should update anything then we should allow user to update anything that's but in
Chun Shao: Mhm. Well uh well it's it's very hard like okay let's say the the user upload uh okay create a underwriting without any document and some processor were already running because some process is not relied on document for example clear business report they don't rely on any document you just you get a and if you prevent them to do the update because it's processing it will be like a wait five six minutes then it will be opened again they can upload documents that's not fair so they can upload documents simultaneous even there is a process running it will not affect the upload of the documents and uh create other you know uh processor executions


02:25:37

Adrees Muhammad: Like in that case if uh we need any document so it just time out and it makes the uh status missing and just we just uh notify the user that we need document and uh the status of the underwriting is now missing. And if the docu user reupload uh upload the document then it starts again or so we can do that.
Chun Shao: Okay. Um I'm not quite understand like in our design we will okay once they upload and create the underwriting we will not uh inform the underwriter anything until suggestion being given. Okay that time we only call a web hook.
Adrees Muhammad: Yeah, we could.
Chun Shao: So during this time uh the user the underwriter must to refresh the status of this underwriting uh from their end we will not push any information to them. Okay.
Adrees Muhammad: Yeah, that's correct.
Chun Shao: Yeah.
Adrees Muhammad: Uh, but I think it's necessary to notify the user what's wrong with this application. What's the status?
Chun Shao: Okay.
Adrees Muhammad: Why? What what's happening? So, it's important to notify the user whether we need to introduce a new property uh of uh uh like in the table or uh in some way we should notify that.


02:27:02

Adrees Muhammad: That's important because maybe something happened while the processing is asynchronous. So it will take some time because of any reason. So it can fail. So we need to notify that.
Chun Shao: Mhm.
Adrees Muhammad: So and uh back to uh the previous part like uh uh as I said like let's say if the processor take five seconds and uh it needs any document so it just time out. If we didn't provide the document, it just time out and uh we just close our process and uh we make the maybe make the status as missing or something and uh we have a message as well with the document missing or something like that and on front end the user will see oh yeah the documents are missing.
Chun Shao: Oh, okay.
Adrees Muhammad: Okay. So I need to upload the document. He just upload the document and the underwriting will re uh resume or you can say restart and uh in that way maybe the process is a bit simpler.
Chun Shao: Okay. Oh, okay. I understand what we're talking about.


02:28:03

Chun Shao: So, if that's the case, the processor will not create any execution. No. So, the execution will not be hold there like uh waiting for the reply. If they don't provide enough information the payload provided for like a to generate a execution list will return a empty. So if the if the user only like a create underwriting without any documents. So it will only run like a couple processors clear report industry processor application processor all the other processes there will be no execution there no need for to inform.
Adrees Muhammad: Yeah, that's Yeah, that's fine.
Chun Shao: So so for the yeah s evaluation like a it's just the status will be like a missing data. Okay.
Adrees Muhammad: Yeah.
Chun Shao: Yeah.
Adrees Muhammad: Yeah, that's fine.
Chun Shao: And uh the Yeah, that's fine.
Adrees Muhammad: Um so uh so yeah in that case uh the pro uh the information we have and let's say uh in the application form uh the processor belongs to that will be executed and just uh the the application execution
Chun Shao: So So it doesn't affect anything.


02:29:24

Adrees Muhammad: will be closed and uh the status will become let's say missing and we just uh uh notify yeah or in some sense we can just notify the user he needs to upload the documents to further proceed or something like that.
Chun Shao: I I okay I don't think we need to notify the user because this is not any error or anything. It's just a maybe the laten latency they didn't receive the documents. Okay. So but yeah we we will have the status uh in the database and uh yeah we can we can remind the underwriter okay this is in the f this is not in this version uh like in the future maybe okay this uh underwriting has been created and uh remains in missing data status for three days. Okay. And uh do you want to take care of it like a reminder or notifications? Yeah, we can do that later. Yeah. But I don't think like uh uh we need to uh like immediately we we we send something like when they create it and we send back any message like oh you missed data something like that.


02:30:51

Chun Shao: It's it's not necessary.
Adrees Muhammad: Yeah, that makes sense. I just uh wanted to yes clarify that concept in my mind like is it feasible to allow user while the application is in process to change anything regarding the application.
Chun Shao: Okay. Mhm.
Adrees Muhammad: So that's the that's why I just uh give that examples.
Chun Shao: Yeah. Yeah. Yeah.
Adrees Muhammad: So that's a bit Yeah.
Chun Shao: Yeah. Yeah. Yeah. No problem. Yeah. Okay. Have another meeting. Yeah. Okay. Sure. All right. Good. Um so Jude uh please okay update the flowchart everything and uh let's talk again probably next um Monday. Is that okay? Do you have enough time to update everything?
Jude Pineda: Uh I'll I I'll charge June. Yeah. I just want to ask you uh is this uh payload enough for the execution update?
Chun Shao: Okay, processor underwriting ID. Okay, probably okay. If you ask me, I would say just the execution um ID will be enough.


02:32:23

Chun Shao: I mean, it's it should be uh Yeah. Okay. Um probably use processor ID like a the underwriting process ID instead of the processor key.
Jude Pineda: Okay.
Chun Shao: Yeah. Yeah. That's the Yeah.
Jude Pineda: For this specific for the specific underwriting tune, right?
Chun Shao: for this particular underwriting is wronging uh yeah process ID and uh yeah other information you can keep it there but actually what we will do is we just uh based on this processor we will run the aggregation so
Jude Pineda: Okay.
Chun Shao: if you don't have anything else you just have this underwriting process ID that'll be good enough but I would say yeah Um yeah, keep the keep the execution ID. Uh it could Yes. So um yeah.
Jude Pineda: So is there any instance that we can uh update the active current executions like uh multiple executions Thanks.
Chun Shao: Okay. So if it's like a bank statement and I have multiple executions and you right click one and uh Okay. I set this execution as the most updated one.


02:33:51

Chun Shao: Okay. The API will receive okay uh this execution ID. Okay. And uh because from the execution ID you can find which process ID it belongs to. Okay. And what's the document ID? Anything. So they will do the replacement. And what they need to tell you, inform you is this execution ID. Okay? And you use this execution ID, you will get the document ID, everything. And you do the aggregation. Okay? Based on this one. Uh but I mean when you do the aggregation, it's above the level of execution. It's on the level of processor, right? For one bank statement. uh if there is one bank statement updated the whole bank statement processor layer the aggregation will be updated. It's not only this one bank statement but it's the whole like the the monthly average everything is based on each document under this regulation right.
Jude Pineda: Yes.
Chun Shao: So yes I would say um the only information you need is the underwriting process ID but I would say it will not harm for you to get more information.


02:35:15

Jude Pineda: Okay. Okay.
Chun Shao: Okay. Yeah. Okay.
Jude Pineda: Uh yeah, I just want to make sure. So since we said update here, uh does that mean we only run aggregation or what other updates are we going to make for this uh execution processor execution?
Chun Shao: Okay. Say that again.
Jude Pineda: Uh so yeah we we put here update right? are but uh I'm confused. Do do we only run aggregation or like do we also need to update the correct is okay that makes sense now.
Chun Shao: We only run exe we only run aggregation. Yeah.
Jude Pineda: So yeah
Chun Shao: Yeah. Because it doesn't create any execution. It just change the current execution. Okay, probably. Hey, uh address do you think like a can we put it directly on the processor? It's processor update. It's just update its uh execution. So underwriting.processor dot update update.
Jude Pineda: And waiting that processor that Yes.
Chun Shao: Yeah. Okay.
Adrees Muhammad: Yeah, that's better, I
Chun Shao: Okay. Sure. Okay. In this case, you just maybe need the underwriting process ID. That's it. Yeah. You don't care about who is being put as the current, you know,
Jude Pineda: Yeah. Thanks, June. Yeah. Thanks, Adris. Yeah.


Transcription ended after 02:37:35

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.
