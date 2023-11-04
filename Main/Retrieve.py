import Memory

from numpy import dot
from numpy.linalg import norm

def extract_recency(nodes):
  """
  Gets the current Persona object and a list of nodes that are in a 
  chronological order, and outputs a dictionary that has the recency score
  calculated.

  INPUT: 
    persona: Current persona whose memory we are retrieving. 
    nodes: A list of Node object in a chronological order. 
  OUTPUT: 
    recency_out: A dictionary whose keys are the node.node_id and whose values
                 are the float that represents the recency score. 
  """
  recency_vals = [0.99 ** i 
                  for i in range(1, len(nodes) + 1)]
  
  recency_out = dict()
  for count, node in enumerate(nodes): 
    recency_out[node.node_id] = recency_vals[count]

  return recency_out

def extract_importance(nodes):
  """
  Gets the current Persona object and a list of nodes that are in a 
  chronological order, and outputs a dictionary that has the importance score
  calculated.

  INPUT: 
    persona: Current persona whose memory we are retrieving. 
    nodes: A list of Node object in a chronological order. 
  OUTPUT: 
    importance_out: A dictionary whose keys are the node.node_id and whose 
                    values are the float that represents the importance score.
  """
  importance_out = dict()
  for count, node in enumerate(nodes): 
    importance_out[node.node_id] = node.poignancy

  return importance_out

def cos_sim(a, b): 
  """
  This function calculates the cosine similarity between two input vectors 
  'a' and 'b'. Cosine similarity is a measure of similarity between two 
  non-zero vectors of an inner product space that measures the cosine 
  of the angle between them.

  INPUT: 
    a: 1-D array object 
    b: 1-D array object 
  OUTPUT: 
    A scalar value representing the cosine similarity between the input 
    vectors 'a' and 'b'.
  
  Example input: 
    a = [0.3, 0.2, 0.5]
    b = [0.2, 0.2, 0.5]
  """
  return dot(a, b)/(norm(a)*norm(b))

def extract_relevance(nodes, focal_pt): 
  """
  Gets the current Persona object, a list of nodes that are in a 
  chronological order, and the focal_pt string and outputs a dictionary 
  that has the relevance score calculated.

  INPUT: 
    persona: Current persona whose memory we are retrieving. 
    nodes: A list of Node object in a chronological order. 
    focal_pt: A string describing the current thought of revent of focus.  
  OUTPUT: 
    relevance_out: A dictionary whose keys are the node.node_id and whose values
                 are the float that represents the relevance score. 
  """
  focal_embedding = Memory.get_embedding(focal_pt)

  relevance_out = dict()
  for count, node in enumerate(nodes): 
    node_embedding = node.embedding[1]
    relevance_out[node.node_id] = cos_sim(node_embedding, focal_embedding)

  return relevance_out


def normalize_dict_floats(d, target_min, target_max):
  """
  This function normalizes the float values of a given dictionary 'd' between 
  a target minimum and maximum value. The normalization is done by scaling the
  values to the target range while maintaining the same relative proportions 
  between the original values.

  INPUT: 
    d: Dictionary. The input dictionary whose float values need to be 
       normalized.
    target_min: Integer or float. The minimum value to which the original 
                values should be scaled.
    target_max: Integer or float. The maximum value to which the original 
                values should be scaled.
  OUTPUT: 
    d: A new dictionary with the same keys as the input but with the float
       values normalized between the target_min and target_max.

  Example input: 
    d = {'a':1.2,'b':3.4,'c':5.6,'d':7.8}
    target_min = -5
    target_max = 5
  """
  min_val = min(val for val in d.values())
  max_val = max(val for val in d.values())
  range_val = max_val - min_val

  if range_val == 0: 
    for key, val in d.items(): 
      d[key] = (target_max - target_min)/2
  else: 
    for key, val in d.items():
      d[key] = ((val - min_val) * (target_max - target_min) 
                / range_val + target_min)
  return d

def top_highest_x_values(d, x):
  """
  This function takes a dictionary 'd' and an integer 'x' as input, and 
  returns a new dictionary containing the top 'x' key-value pairs from the 
  input dictionary 'd' with the highest values.

  INPUT: 
    d: Dictionary. The input dictionary from which the top 'x' key-value pairs 
       with the highest values are to be extracted.
    x: Integer. The number of top key-value pairs with the highest values to
       be extracted from the input dictionary.
  OUTPUT: 
    A new dictionary containing the top 'x' key-value pairs from the input 
    dictionary 'd' with the highest values.
  
  Example input: 
    d = {'a':1.2,'b':3.4,'c':5.6,'d':7.8}
    x = 3
  """
  top_v = dict(sorted(d.items(), 
                      key=lambda item: item[1], 
                      reverse=True)[:x])
  return top_v


def new_retrieve(person, focal_points, n_count=30): 
  """
  Given the current individual and focal points (focal points are events or 
  thoughts for which we are retrieving), we retrieve a set of nodes for each
  of the focal points and return a dictionary. 

  INPUT: 
    persona: The current individual object whose memory we are retrieving. 
    focal_points: A list of focal points (string description of the events or
                  thoughts that is the focus of current retrieval).
  OUTPUT: 
    retrieved: A dictionary whose keys are a string focal point, and whose 
               values are a list of Node object in the agent's associative 
               memory.

  Example input:
    individual = <individual> object 
    focal_points = ["How are you?", "Jane is swimming in the pond"]
  """
  # <retrieved> is the main dictionary that we are returning
  retrieved = dict() 
  for focal_pt in focal_points: 
    # Getting all nodes from the agent's memory 
    nodes = []
    
    for memory in person.memorystream:
        nodes.insert(0,memory)
        
    # Calculating the component dictionaries and normalizing them.
    recency_out = extract_recency(nodes)
    recency_out = normalize_dict_floats(recency_out, 0, 1)
    importance_out = extract_importance(nodes)
    importance_out = normalize_dict_floats(importance_out, 0, 1)  
    relevance_out = extract_relevance(nodes, focal_pt)
    relevance_out = normalize_dict_floats(relevance_out, 0, 1)

    # Computing the final scores that combines the component values. 
    # Note to self: test out different weights. [1, 1, 1] tends to work
    # decently, but in the future, these weights should likely be learned, 
    # perhaps through an RL-like process.
    # gw = [1, 1, 1]
    # gw = [1, 2, 1]
    gw = [0.5, 3, 2]
    master_out = dict()
    for key in recency_out.keys(): 
      master_out[key] = recency_out[key]*gw[0] + relevance_out[key]*gw[1] + importance_out[key]*gw[2]

    # Extracting the highest x values.
    # <master_out> has the key of node.id and value of float. Once we get the 
    # highest x values, we want to translate the node.id into nodes and return
    # the list of nodes.
    master_out = top_highest_x_values(master_out, n_count)
    master_nodes = []
    
    for key,value in master_out:
        master_nodes.append(person.memstream.get_concept_node_by_id(id))

    #Add the part to change the last access time to current time
      
    retrieved[focal_pt] = master_nodes

  return retrieved