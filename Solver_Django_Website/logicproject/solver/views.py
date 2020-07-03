from django.shortcuts import render
from django.http import HttpResponse
from .logic_solver import (Kripke, 
						   analyse, 
						   ParsingError, 
						   ModelError, 
						   PropositionError, 
						   ModelParsingError,
						   Formula
						   )
from .graph import Graph

import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
import math
# Create your views here.

example_model = Kripke()
example_model.assign_model('{"real_world": 1, "R": {"a": [[1, 2], [1, 3], [2, 2], [3, 3],[2,3],[3,2]], "b": [[1,3],[2,3],[3,3]], "c": [[1,1],[2,2],[3,3],[3,1],[1,3]]}, "V": {"q": [3], "p": [2,3], "r": [1,2,3]}}')

def home(request):
	# Base case page without solution printed
	model = example_model.dict_str_representation()
	modelExpl = str(example_model)
	context = {'model': model, 'modelExpl': modelExpl}

	return render(request, 'solver/dashboard.html', context)

def home_solution(request):

	context = {}

	# Save current values (may be updated later)
	if request.POST.get('model'):
		model = str(request.POST['model'])
		context['model'] = model
	if request.POST.get('phi'):
		phi = str(request.POST['phi'])
		context['phi'] = phi

	print(request.POST)

	if request.POST.get('options') == 'general':
		eval_mode = 'general'  # Everyone knows
		#context['ek'] = '-'
		print('Everyone knows')
	else:
		eval_mode = 'common'  # Common belief (default)
		#context['cb'] = '-'
		print('Common belief')

	context['eval_mode'] = eval_mode

	try:
		M = Kripke()
		M.assign_model(model.strip())
		context['modelExpl'] = str(M)
		
		if request.POST.get('visBtn'):
			# Model is valid and shall be rendered
			context['graphModel'] = return_graph(M)	
		
		if request.POST.get('phi'):
			# Add interpretation of formula
			context['modelExpl'] += ('\nInput formula interpreted as: ' +
			 						  str(Formula(phi)))

			sol = analyse(M, phi, eval_mode)

			if sol:
				# Solution has been found
				(S, agent_to_rem) = sol[0]
				solution = S.dict_str_representation()
				print("Solution ", solution)
				context['solution'] = solution

				if agent_to_rem:
					# Solution involves removing at least one agent
					context['solutionExpl'] = str(S) + 'Agent(s) removed: ' + str(agent_to_rem)
				else:
					# Solution involves removing at least one agent
					context['solutionExpl'] = str(S) + 'No agent has to be removed.'

				if request.POST.get('visBtn'):
					# Solution is valid and can be plotted
					context['graphSolution'] = return_graph(S)
			else:
				# No solution found
				print("Solution ", 'There exists no solution.')
				context['solution'] = 'There exists no solution.'

		else:
			# No formula to be established as common belief has been provided
			print('Please provide query formula!')
			context['completenessWarning'] = 'Please provide query formula!'
			

	# Battery of error handling
	except ModelParsingError as e:
		# Model syntax invalid
		print('Error:', e)
		context['invalidInput'] = str(e)
	except ParsingError as e:
		# Invalia proposition
		print('Error:', e)
		context['invalidInput'] = str(e)
	except PropositionError as e:
		# Proposition not in language
		print('Error:', e)
		context['invalidInput'] = str(e)
	except ModelError as e:
		# Invalid model
		print('Error:', e)
		context['invalidInput'] = str(e)
	except Exception as e:
		print('Please check syntax!')
		context['invalidInput'] = 'Please check syntax! Error message: ' + str(e)


	return render(request, 'solver/dashboard.html', context)


def return_graph(model):
	# Visualization of Kripke model:

	g = Graph()

	accessibilities, valuations = model.summarize_model()

	print('agents', model.agents)
	print('states', model.S)
	print('propositions', model.P)
	print('accessibilities', accessibilities)
	print('valuations', valuations)

	g = Graph()
	g.add_nodes(valuations)
	g.add_edges(accessibilities)
	fig = g.visualize(html=True)

	# Don't touch - Convert plot to html img
	imgdata = StringIO()
	fig.savefig(imgdata, format='svg')
	imgdata.seek(0)  # rewind the data

	data = imgdata.getvalue()

	return data
