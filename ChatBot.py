
# coding: utf-8

# In[29]:


from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
training_data = load_data('./data/demo-rasa.json')
trainer = Trainer(config.load('./data/config_spacy.yml'))
trainer.train(training_data)
model_directory = trainer.persist('./data/Model')  # Returns the directory the model is stored in


# In[30]:


from rasa_nlu.model import Metadata, Interpreter

# where `model_directory points to the folder the model is persisted in
interpreter = Interpreter.load(model_directory)





# In[34]:


interpreter.parse(u'please open cricket')


# In[ ]:




