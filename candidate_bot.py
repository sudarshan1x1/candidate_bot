from botbuilder.core import ActivityHandler, TurnContext, ConversationState,MessageFactory
from botbuilder.schema import ActivityTypes, ChannelAccount
from botbuilder.dialogs import DialogSet,WaterfallDialog,WaterfallStepContext 
from botbuilder.dialogs.prompts import ( 
    TextPrompt, 
    NumberPrompt, 
    PromptOptions, 
    ChoicePrompt,
    PromptValidatorContext
)
from botbuilder.dialogs.choices import Choice
from c_model import Model

class CandidateBot(ActivityHandler):

    def __init__(self,conversation : ConversationState) :
        self.profileinfo = None
        self.constate = conversation
        self.state_prop = self.constate.create_property("dialog_set")
        self.dialogset = DialogSet(self.state_prop)
        self.dialogset.add(TextPrompt("text_prompt"))
        self.dialogset.add(NumberPrompt("number_prompt", self.IsValidMobileNumber))
        self.dialogset.add(NumberPrompt("salary_prompt"))
        self.dialogset.add(ChoicePrompt(ChoicePrompt.__name__))
        self.dialogset.add(WaterfallDialog("main_dialog",
        [self.get_name,self.get_phone_number,self.get_email,self.get_education,self.get_field,self.get_designation,
        self.get_workexp,self.role,self.roles,self.tech_stack,self.location,self.current_salary,self.end_dialog]))
        self.model = Model()

    async def welcome_user(self, turn_context: TurnContext):
        if turn_context.activity.text is None :
            await turn_context.send_activity("Hello! Welcome to QuodeWorks. I'm here to help you with your onboarding process. Let's get started, shall we?")
        if turn_context.activity.text:
            await self.on_turn(turn_context)
        
        return self.profileinfo

    async def IsValidMobileNumber(self, prompt_valid: PromptValidatorContext):
        if (prompt_valid.recognized.succeeded is False):
            await prompt_valid.context.send_activity("Please Enter Only Numbers")
            return False
        else : 
            value = str(prompt_valid.recognized.value)
            if len(value) < 10:
                await prompt_valid.context.send_activity("Please Enter a valid phone number")
                return False
            
        return True


    async def get_name(self,waterfall_step: WaterfallStepContext):
        return await waterfall_step.prompt("text_prompt",
        PromptOptions(prompt=MessageFactory.text(" Enter your Full Name")),)

    async def get_phone_number(self,waterfall_step: WaterfallStepContext):
        waterfall_step.values['name']= waterfall_step._turn_context.activity.text
        return await waterfall_step.prompt("number_prompt",
        PromptOptions(prompt=MessageFactory.text("Enter your Mobile Number")))

    async def get_email(self,waterfall_step: WaterfallStepContext):
        waterfall_step.values['mobile'] = waterfall_step._turn_context.activity.text
        return await waterfall_step.prompt("text_prompt",
        PromptOptions(prompt=MessageFactory.text("Enter your Email Id")))

    async def get_education(self,waterfall_step: WaterfallStepContext):
        waterfall_step.values['email'] = waterfall_step._turn_context.activity.text
        listofchoice = [Choice("Diploma"), Choice("Bachelor's Degree"), Choice("Master's Degree"), Choice("Doctoral Degree")]
        return await waterfall_step.prompt(ChoicePrompt.__name__,
        PromptOptions(prompt=MessageFactory.text("What is the highest level of education you have completed?"),choices=listofchoice))
    
    async def get_field(self, waterfall_step: WaterfallStepContext):
        waterfall_step.values['education']= waterfall_step.result.value
        return await waterfall_step.prompt("text_prompt",
        PromptOptions(prompt=MessageFactory.text("Enter the field you've obtained your highest Degree in")))
           
    async def get_designation(self,waterfall_step: WaterfallStepContext):
        waterfall_step.values['field'] = waterfall_step._turn_context.activity.text
        return await waterfall_step.prompt('text_prompt', 
        PromptOptions(prompt=MessageFactory.text("What is your current job title/ role ?")))
    
    async def get_workexp(self,waterfall_step: WaterfallStepContext):
        waterfall_step.values['designation']= waterfall_step._turn_context.activity.text
        listofchoice = [Choice("Fresher"), Choice("1-2 years"), Choice('3-5years'), Choice('5-8 years'), Choice('8+ years')]
        return await waterfall_step.prompt(ChoicePrompt.__name__,
        PromptOptions(prompt=MessageFactory.text("Select your Work-Experience"),choices=listofchoice))
       
    async def role(self,waterfall_step: WaterfallStepContext):
        waterfall_step.values['work_exp'] = waterfall_step.result.value
        listofchoice = [Choice("Internship"), Choice("Full-time")]
        return await waterfall_step.prompt(ChoicePrompt.__name__,
        PromptOptions(prompt=MessageFactory.text("Which Role are you applying For? "),choices=listofchoice))
    
    async def roles(self,waterfall_step: WaterfallStepContext):
        role = waterfall_step.result.value
        if role == 'Internship' :
            listofchoice = [Choice("AI/ML Intern"), Choice("Software Developer Intern")]
        elif role == 'Full-time':
            listofchoice = [Choice('AI/ML engineer'), Choice("Software Developer Engineer")]
        
        return await waterfall_step.prompt(ChoicePrompt.__name__,
        PromptOptions(prompt=MessageFactory.text("These are the available Roles for you"),choices=listofchoice))
    
    async def tech_stack(self,waterfall_step: WaterfallStepContext):
        waterfall_step.values['role'] = waterfall_step.result.value
        listofchoice = [Choice('.NET'),Choice('PHP'), Choice('Full-Stack'), Choice('Azure')]
        return await waterfall_step.prompt(ChoicePrompt.__name__,
        PromptOptions(prompt=MessageFactory.text("Select your tech stack "),choices=listofchoice))
    
    async def location(self,waterfall_step: WaterfallStepContext):
        waterfall_step.values['tech_stack'] = waterfall_step.result.value
        listofchoice = [Choice('On-Location'), Choice('Remote-Work')]
        return await waterfall_step.prompt(ChoicePrompt.__name__,
        PromptOptions(prompt=MessageFactory.text("What is your mode of work preference?"),choices=listofchoice))

    
    async def current_salary(self,waterfall_step:WaterfallStepContext):
        waterfall_step.values['location'] = waterfall_step.result.value
        return await waterfall_step.prompt('salary_prompt', 
        PromptOptions(prompt=MessageFactory.text("Could please provide your Current Salary Expectations?")))
        
    async def end_dialog(self, waterfall_step: WaterfallStepContext):
        waterfall_step.values['current_salary'] = waterfall_step._turn_context.activity.text
        self.profileinfo = {
            "Name": waterfall_step.values['name'],
            "Phone no": waterfall_step.values['mobile'],
            "Email": waterfall_step.values['email'],
            "Education": waterfall_step.values['education'],
            "Field": waterfall_step.values['field'],
            "Designation": waterfall_step.values['designation'],
            "Work Experience": waterfall_step.values['work_exp'],
            "Role": waterfall_step.values['role'],
            "Tech Stack": waterfall_step.values['tech_stack'],
            "Location": waterfall_step.values['location'],
            "Current Salary": waterfall_step.values['current_salary']
            }
        await waterfall_step.end_dialog()
        
    
    async def on_turn(self, turn_context: TurnContext):
        dialog_context = await self.dialogset.create_context(turn_context)

        if (dialog_context.active_dialog is not None):
        # If the dialog is active, continue with it
            await dialog_context.continue_dialog()

        else:
        # If the dialog is not active, start the main dialog
            await dialog_context.begin_dialog("main_dialog")

        await self.constate.save_changes(turn_context)
    
    


