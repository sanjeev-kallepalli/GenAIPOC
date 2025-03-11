Follow these steps to run the code

Step1:
  In a directory where you want have cloned the repo create a virtual enviroment.

  """
  python -m venv .venv
  """
  once the virtual environment is created activate by using below and you should see (.venv) in root path.
  """
  .venv/Scripts/activate
  """
  Now install all requirements that is needed.
  """
  pip install -r ./app/requirements.txt
  """
Step2:
  To use the FastAPI service run below command after Step1.
  create .env file under app folder and add credentials.
  """
  OPENAI_API_KEY=<yourkey>
  OPENAI_ORGANIZATION=<yourorg>
  """
  """
  cd app
  uvicorn main:app --host 0.0.0.0 --port 8080
  """
  You may use Postman now to directly invoke and test. But just in case you need a complete Bot feel go to step 3.
Step3:
  Run the simple UI for invoking LLM and uploading document.
  in a new terminal, after activing virtual environment as step1 execute below
  """
  cd frontend
  python -m http.server
  """
  

  
