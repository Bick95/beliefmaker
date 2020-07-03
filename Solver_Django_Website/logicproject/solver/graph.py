import numpy as np

import math

from matplotlib import patches
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import operator

################################################################################
################################################################################
############################### HELPER FUNCTIONS ###############################
################################################################################
################################################################################

def vector_arithmetics(vec, modifier, val=None):
  # Define math operators
  ops = { "+": operator.add, 
          "-": operator.sub,
          "mod": operator.mod,
          "%": operator.mod,
          "/": operator.truediv,
          "*": operator.mul,
          "pow": operator.pow,
          "norm": "norm"
         }

  # Prepare vector operation
  assert(isinstance(modifier, str))
  vec = np.asarray(vec)

  if modifier == "norm":
    return vec / np.sum(np.abs(vec))

  # val can only be none for normalization
  if val is not None:

    # Retrieve math operator
    op = ops[modifier]

    if not (isinstance(val, tuple) or isinstance(val, list)):
      # Modifier is a scalar
      return op(vec, val)
    
    # Modifier is itself vector
    val = np.asarray(val)
    return op(vec, val)

    raise ValueError('val cannot be none, except when normalizing vec!')


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    # Thanks to: https://stackoverflow.com/a/34374437/11478452
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


################################################################################
################################################################################
################################# GRAPH CLASS ##################################
################################################################################
################################################################################

class Graph():
  def __init__(self):
    self.nodes = {}   # {node_id: sattelite_data}
    self.edges = {}   # {edge_id: sattelite_data}

  def add_nodes(self, nodes, attributes=None):
    # Assign self.nodes, where self.nodes is a dict of form: {node_id: sattelite_data}
    if attributes:
      assert(isinstance(nodes, list))
      assert(len(nodes) == len(attributes))
      self.nodes = {nodes[i]: attributes[i] for i in range(len(nodes))}
    elif isinstance(nodes, list):
      self.nodes = {node: None for node in nodes}
    else:
      assert(isinstance(nodes, dict))
      self.nodes = nodes

  def add_edges(self, edges, attributes=None):
    # Assign self.edges, where self.edges is a dict of form: {edge_id: sattelite_data}
    if attributes:
      assert(isinstance(edges, list))
      assert(len(edges) == len(attributes))
      self.edges = {edges[i]: attributes[i] for i in range(len(edges))}
    elif isinstance(edges, list):
      self.edges = {node: None for node in edges}
    else:
      assert(isinstance(edges, dict))
      self.edges = edges

  def add_node(self, node, attribute=None):
    # May overwrite existing node
    self.nodes[node] = attribute

  def add_edge(self, edge, attribute=None):
    # May overwrite existing edge
    self.edges[edge] = attribute
  
  def delete_node(self, node):
    # TODO: haven't tested/checked yet. Focus was primarily on visualizing so far
    raise Warning('Untested function delete_node.')
    del self.nodes[node]
    for edge in self.edges:
      if node in edge:
        del edge
  
  def delete_edge(self, edge):
    # TODO: haven't tested/checked yet. Focus was primarily on visualizing so far
    raise Warning('Untested function delete_edge.')
    for e in self.edges:
      if e == edge:
        del e
        break
  
  def visualize(self, html=False):
    # Enumerate nodea and edges in order & in reversed order
    enumerated_nodes = {i: n for i, n in enumerate(sorted(self.nodes))}
    enumerated_edges = {i: e for i, e in enumerate(sorted(self.edges))}
    rev_enumerated_nodes = {n: i for i, n in enumerate(sorted(self.nodes))}
    rev_enumerated_edges = {e: i for i, e in enumerate(sorted(self.edges))}

    # Plot nodes - They will lie equidistantly distributed along an outer circle
    colors = (0,0,0)
    nodes = len(self.nodes)
    step_size = 360/nodes
    thetas = np.arange(0,360,step_size)  # Angles at which nodes lie on outer radius
    add = 0 if len(self.nodes.keys()) < 5 else 20 * len(self.nodes.keys())
    r_min = 40 + add   # Min radius of outer circle along which points lie
    print('NR NODES:', (len(self.nodes.keys())-3), self.nodes, self.nodes.keys())
    d = 2*r_min   # Corresponding Diameter
    # Adaptively choose actual diameter of outer circle
    if len(thetas) <= 2:
      r_maj = d
    else:
      d_s = math.pow(d,2)
      d_1 = math.pow(math.cos(np.deg2rad(thetas[1]))-1, 2)
      d_2 = math.pow(math.sin(np.deg2rad(thetas[1])), 2)
      r_maj = math.sqrt(d_s / (d_1 + d_2))

    x = [math.cos(np.deg2rad(t))*r_maj for t in thetas]
    y = [math.sin(np.deg2rad(t))*r_maj for t in thetas]

    # Create figure
    fig = plt.figure()

    # Place nodes in graph/figure
    plt.scatter(x, y, c='lightblue', alpha=0.8, s=r_maj*7)
    plt.margins(0.2)

    # Print nodes' satellite data to plot -- Done below to prevent it from being overwritten by edge-labels
    #for i in range(len(self.nodes)):
    #  string = str(enumerated_nodes[i]) + '\n' + ','.join(self.nodes[enumerated_nodes[i]])
    #  plt.text(x[i]*1., y[i]*1., string, horizontalalignment='center', verticalalignment='center', weight="bold")

    # Edge visualization
    style="wedge"
    kw_lin = dict(arrowstyle=style, shrinkA = 0, shrinkB = 0, color="#808080", label='', connectionstyle="arc3,rad=.15")
    style="simple,head_width=5,head_length=8"
    kw_arw = dict(arrowstyle=style, shrinkA = 0, shrinkB = 0, color="#808080", label='', connectionstyle="arc3,rad=.15")

    # Visualize non-reflexive edges
    for i in range(len(self.edges)):
      edge = enumerated_edges[i]
      if edge[0] != edge[1]:
        # Determinin in between which two nodes edge is to be drawn (A -> B)
        ptA = (x[rev_enumerated_nodes[edge[0]]], y[rev_enumerated_nodes[edge[0]]])
        ptB = (x[rev_enumerated_nodes[edge[1]]], y[rev_enumerated_nodes[edge[1]]])

        ## Determine where the Edge label is to be drawn ##

        # Determine mid point in between nodes
        mid = vector_arithmetics(ptA, '+', ptB)
        mid = vector_arithmetics(mid, '/', 2)
        #plt.plot(mid[0], mid[1], 'ro')
        
        # Get the normalized vector in direction A --> B
        dirA = vector_arithmetics(ptA, '-', mid)
        norm_dirA = vector_arithmetics(dirA, 'norm')

        # Determine a point close to mid point in between A and B
        mid_close = vector_arithmetics(mid, '+', norm_dirA)
        #plt.plot(mid_close[0], mid_close[1], 'bo')

        # Rotate the mid point by -90 deg around the close by point mid_close
        # in order to get a vector orthoginal to the line connecting A and B
        mid_rotated = rotate(mid_close, mid, math.radians(-90))
        #plt.plot(mid_rotated[0], mid_rotated[1], 'yo')

        # Get the vector orthogonal to line/vector A-->B as described above
        displacement_dir = vector_arithmetics(mid_rotated, '-', mid_close)
        displacement_dir = vector_arithmetics(displacement_dir, 'norm')  # wrt origin

        # Scale the vector orthogonal to A --> B a bit up
        add = 0 if len(self.nodes.keys()) < 5 else 20 * len(self.nodes.keys())
        scaling_factor = 10. + add
        scaled_displacement = vector_arithmetics(displacement_dir, '*', scaling_factor)

        # Take the peak of the scaled vector orthogonal to A --> B to be the 
        # new pseudo-mid-point where the edge label is to be drawn
        new_mid = vector_arithmetics(mid_close, '+', scaled_displacement)

        # Update mid point to non-overlapping (with inverse directional edge) position 
        mid = new_mid

        # Draw the two arrows A --> mid --> B
        a = patches.FancyArrowPatch(ptA, mid, **kw_lin)
        b = patches.FancyArrowPatch(mid, ptB, **kw_arw)
        plt.gca().add_patch(a)
        plt.gca().add_patch(b)

        #plt.text(mid[0], mid[1], self.edges[edge], 
        #         horizontalalignment='center', 
        #         verticalalignment='center')

        # Plot the edge label and place a point at label position to enforce 
        # that the text does not fall out of rendered area
        bbox_props = dict(boxstyle="round,pad=0.3", fc="lightgray")#, ec="b", lw=2)
        plt.plot(mid[0], mid[1])  # Set fake point to make sure text is not going to end up outside plotted region 
        plt.text(mid[0], mid[1], ','.join(self.edges[edge]), ha="center", va="center", bbox=bbox_props)
        
    # Visualize reflexive edges
    for i in range(len(self.edges)):
      edge = enumerated_edges[i]

      # Select only reflexive edges here
      if edge[0] == edge[1]:
        # Get node corresponding to reflexive edge
        pt = (x[rev_enumerated_nodes[edge[0]]], y[rev_enumerated_nodes[edge[0]]])

        # Get direction into which reflexive edge is going to be drawn:
        # Going to be out of the outer circle along which all nodes lie
        pt_dir = vector_arithmetics(pt, 'norm')
        add = 0 if len(self.nodes.keys()) < 5 else 20 * len(self.nodes.keys())
        scaling_factor = 30. + add
        scaled_pt_dir = vector_arithmetics(pt_dir, '*', scaling_factor)  # Scale direction, determine distance of label from node

        # Determine text position
        text_pos = vector_arithmetics(pt, '+', scaled_pt_dir)

        # Draw two edges A --> text pos --> A
        a = patches.FancyArrowPatch(pt, text_pos, **kw_lin)
        b = patches.FancyArrowPatch(text_pos, pt, **kw_arw)
        plt.gca().add_patch(a)
        plt.gca().add_patch(b)

        # Plot the edge label and place a point at label position to enforce 
        # that the text does not fall out of rendered area
        plt.plot(text_pos[0], text_pos[1]) # Set fake point to make sure text is not going to end up outside plotted region 
        bbox_props = dict(boxstyle="round,pad=0.3", fc="lightgray")#, ec="b", lw=2)
        plt.text(text_pos[0], text_pos[1], ','.join(self.edges[edge]), ha="center", va="center", 
                 #rotation=45, size=15,
            bbox=bbox_props)

    # Print nodes' satellite data to plot (to prevent it from being overwritten by some edge-labels)
    for i in range(len(self.nodes)):
      string = str(enumerated_nodes[i]) + '\n' + ','.join(self.nodes[enumerated_nodes[i]])
      plt.text(x[i]*1., y[i]*1., string, horizontalalignment='center', verticalalignment='center', weight="bold")

    # Don't render axes
    plt.axis('off')

    # If used for generating graphs to be shown on html page, only return fig w/o rendering
    if html:
      return fig
    
    plt.show()


