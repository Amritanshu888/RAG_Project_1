- How we are specifically going to create Pipelines, integrate it in a modular coding fashion --> important for building a end-to-end project.
- The documents which we will have we will completely execute the pipeline wherein we are able to convert this into vectors and then store it in some kind of vectorstores.
- Pattern Followed: Modular Coding Pattern
- Using UV Package manager for building the entire project.

## UV Package Manager
- In terminal write: uv init ---> I m going to initialize this entire workspace for that we basically use "uv init" command.
- Use this command in the terminal in ur present working directory where u are creating ur project.
- Once we do this in ur present working directory by default some of the files will be created.
- U go to pyproject.toml file which got created in ur present working directory, there it will show that it requires python version greater than or equal to 3.12
- Along with this README.md file will get created.
- Here u have initialized a workspace.

- Once u initialize a workspace the next thing is that u create a virtual environment for project.
- The reason for creating virtual environment for project is that whatever library u actually require u will be doing the installation over here.
- Command: uv venv ---> This will basically be my virtual environment.
- The above command will help us create our virtual environment.
- Once u create this a '.venv' folder will be created in ur present working directory.
- This is what my virtual environment is.

- Now we have to activate the virtual environment:
- When we use u can also use 'pip' to create the virtual environment, but this is more faster when compared to pip, that is one of the advantages that we got from using uv.
- When u will execute this command: 'uv venv' u will automatically get the command to activate the virtual environment, it will be denoted with 'Activate with:' following the command, use this command to activate the virtual environment.
- Once u do this ur virtual environment will be activated.

- After this we will create a file called as requirements.txt file where we will write all the requirements.
- Then inorder to install all these libraries we have the command: uv add -r requirements.txt
- In pip we had the command: pip install -r requirements.txt
- uv is very very much faster as compared to pip hence highly recommended, hence u will quickly be able to do things over here.
- Further we can add more packages in our environment by using the following command, like if i have to add 'ipykernel' the command will be: 'uv add ipykernel'
- This is the part where we created our new virtual environment and did the installation of the specific libraries in the requirements.txt file.
- Next we will go ahead and define a project structure.

## LangGraph
- w.r.t langgraph we have nodes, graph builders, so all those things need to be divided in the form of project structure.

## Defining Project Structure
- Building the project structure is really important as this will actually help u to understand that how the entire flow of project gets executed in the form of a pipeline.
- In main/hello .py file we just have the basic information that will help u to execute the code.
- src folder contains all the important components of the pipeline.
- Outer we have main.py file and this will be able to call all the files that are present inside this src folder.

- Anything that exists inside the data folder i will try to read all those informations let it be a txt file, url file, or whatever kind of files u want we have to write a code in data ingestion wherein we read all this particular information and that is what data ingestion and data parsing is all about.

## How to do the coding
- First of all i need to go ahead and develop each and every module independently, and then with the help of graph_builder we will try to integrate everything.
- First we will go ahead with document ingestion, we will read whatever data is present over there in the data folder and then finally we will create our streamlit_app.py

- This same project structure needs to be maintained.
- __init__.py file is there inside each and every folder so that we can import each of these folders as packages.

## Lifecycle of a RAG Project
- First we need to create a pipeline wherein u ingest the data, convert or do the chunking for that particular data and then store everything into the vectorstore or vector databases.
- First we will start with document_ingestion, inside this we have a file named as document_processor.py.
- As per life cycle of a RAG project after creating document ingestion we should be creating a vectorstore, go inside the vectorstore folder and create our file vectorstore.py file. ---> We require some kind of LLM model for the embedding.
- Next we are defining state. When we are developing a langgraph application we need to define our state also.
- Another thing which we require is nodes. First we will define node definition, then we will go and define the graph builder, the graph builder will be having the entire graph from the start to the end about how the execution is going to basically happen.
- When we talk about nodes that same nodes will be used in the graph as a function/functionality.

- In Graph Builder we will be defining our flow.

## What should be the flow of the Application
- What kind of workflow we will specifically use:
- 1st we have our start state, then after this we will have our retriever, then we are going to give this data to generator, whenever we talk about retriever this will always be giving a request to the vectorstore, based on the vectorstore we can go ahead and get the response.
- Once we get the response then we send this response to the generator, here we have some kind of LLM which will be taking the response in the form of the context and then finally we will be generating the output.
- At last we will have our end state.

- So here we are going to generate two different variants, this is one of the simple variants wherein i have a retriever, i get the context(above mentioned response is nothing but context).
- I give the context to the LLM and then finally i generate the output.
- That is my first variant.

## 2nd Variant
- In 2nd variant what i will do is that here only i will create a 'React Agent', whenever we say React Agent that basically means i will be having LLM with Tools.
- So once i get this specific response, i will give that context to my LLM, LLM will have tools binded to it so if it wants to use the tool based on the context it can go ahead and use it and finally generate the output.

- So both of these variants we will go ahead and try to execute it.

- In our graph builder i have a retriever and a generator steps, retriever will give me the context, as soon as i give a query it will first of all go to the retriever and then generator and then we will end the step.

## React Agent Node functionality
- Initially we had only two nodes: retriever and generate answer.
- Inside this generate answer we are just getting the context information along with the prompt and then we are just giving it to our LLM.
- But sometimes if we just want to use a efficient agent like a React Agent, inside this react agent within this particular generator i will be having a LLM and this will be binded with tools, now which tools ??
- Let's say over here my initial request goes to the retriever, like if i just put up a query: What is LLM ??, now as soon as i put up this particular query u will be able to see that first of all it will go to the retriever, from the retriever it will go ahead and hit the vectorstore and vectorstore will go ahead and provide some response, what if the question asked the answer for that question is not available in the vectorstore, then the response that u will be getting the context that u will be getting will not be much more sufficient to answer this particular question, then it will go to the next step i.e. generator, now this generator will take this response as a context and now if it sees that this context is not sufficient what this LLM can do it can go ahead and search from the tools, now this tools can be Wikipedia Tool, Tavily Tool/Search, Duck Duck Go Tool/Search it can be different kinds of tool itself. -----> So this is the reason we want to go ahead and create React Agent Architecture over here, inside my node functionality.
- Inside the nodes folder create a file named as 'reactnode.py'