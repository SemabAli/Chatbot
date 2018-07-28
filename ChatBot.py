
# coding: utf-8

# In[9]:


from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_core.actions import Action
import warnings
warnings.filterwarnings("ignore")

from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.agent import Agent
from rasa_core.policies.memoization import MemoizationPolicy
from policy import RestaurantPolicy



def train_dialogue(domain_file="domain.yml",model_path="./Model/dialogue",training_data_file="Stories.md"):
    agent = Agent(domain_file,policies=[MemoizationPolicy(max_history=5),RestaurantPolicy()])
    training_data = agent.load_data(training_data_file)
    agent.train(training_data,epochs=100,
            batch_size=5,
            validation_split=0.2
    )

    agent.persist(model_path)
    return agent





def train_nlu():
    from rasa_nlu.training_data import load_data
    from rasa_nlu import config
    from rasa_nlu.model import Trainer

    training_data = load_data('./demo-rasa.json')
    trainer = Trainer(config.load("./config_spacy.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('./Model/',fixed_model_name="current")

    return model_directory




# In[11]:


model_directory=train_nlu()



# In[17]:


from rasa_nlu.model import Metadata, Interpreter
# where `model_directory points to the folder the model is persisted in
interpreter = Interpreter.load(model_directory)

interpreter.parse(u'show live match today')


# In[13]:



train_dialogue()





# In[18]:


from rasa_core.agent import Agent
agent = Agent.load('./Model/dialogue', interpreter=model_directory)
print("Your bot is ready to talk! Type your messages here or send 'stop'")
while True:
    a = input()
    if a == 'stop':
        break
    responses = agent.handle_message(a)
    #print (responses)
    for response in responses:
        print(response["text"])

