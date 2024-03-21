from crewai import Agent , Task , Process
from langchain_groq import ChatGroq
from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory , ReadonlysharedMemory
from langchain.prompts import PromptTemplate
from langchain_community import DuckDuckGoSearchRun

I

chat = ChatGroq(temperature=0, groq_api_key ="Your_API_Key" ,name_model="mixtral-8x7b-32768")

template = """This is a conversation between a human and ai agent :
{chat_history}
write a summary of the conversation for {input}:

"""

prompt = PromptTemplate(input_variables=['input',"chat_history"],template=template)
memory = ConversationBufferMemory(memory_key="chat_history")
readonlymemory = ReadonlySharedMemory(memory=memory)
summary_chain = LLMChain(
llm=chat,
prompt=prompt,
verbose=True,
memory=readonlymemory,
)
# Create Tool

search = DuckDuckGoSearchRun()

tool_use = [
Tool(
name="Search",
func=search.run,
description="useful for when you need to answer questions about current Event"

Toolk
name="Swcry",
func=sumn ry_chain.run,
descripti on="useful for when you summarize a conversation. The input to this tool should be a string, representing who will read this summary. The chat history will be used to generate the summary."

),
]

tool_use_1 = [
    Tool(
        summary = "Summary",
        func= summary_chain.run,
        description="useful for when you summarize a conversation. The input to this tool should be a string, representing who will read this summary."
    )
]


#Define Agents

email_author = Agent(
    role= 'Professional Email Author',
    goal="Craft concise and engaging emails",
    backstory='Experienced in writing imapctful marketing emails',
    verbose=True,
    allow_delegation=False,
    llm = chat,
    tools=tool_use_1
)

marketing_strategist = Agent(
    role="Marketing Strategist",
    goal= 'Lead the team in creating effective cold emails',
    backstory='A seasoned Chief Marketing Officer with a Keen eye for standout marketing content.',
    verbose=True,
    allow_delegation=False,
    llm = chat,
    tools=tool_use_1
)

content_specialist = Agent(
    role="Content Specialist",
    goal="Critique and refine email content",
    backstory=" A professional copywriter with a wealth of experience in persausive writing.",
    verbose=True,
    allow_delegation=False,
    llm=chat,
    tools=tool_use_1
)

)

#create A single Crew

# Define Task

email_task = Task(
    description '''1. Generate two distinct variaations of a cold email promopting a video solution.
    2. Evaluate the written emails for thier effectiveness and engagement.
    3. Scrutinize the emails for grammatical correctness and clarity.
    4 Adjust the emails to align with best practices for cold outreach. Consider the feedback provided to the marketing_strategist.
    5. Revise the emails based on all feedback, creating two final versions. ''',
    agent=marketing_strategist # The marketing Strategist is in Charge and can delegate
    agents = [email_author,marketing_strategist,content_specialist],
    tasks = [email_task],
    verbose = True,
    process = Process.sequential

)
#create A single Crew

email_crew = Crew(
    agents = [email_author,marketing_strategist, content_specialist],
    tasks = [email_task],
    verbose = True,
    process = Process.sequential

)

#Execution Flow
print("Crew: Working on Email Task")
emails_output = email_crew.kickoff()
