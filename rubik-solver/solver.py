# Jonathan Bergen
from rubik import *
import collections as col


# helper functions
def tryPerm(pos, move, path, hash_table):

	# apply the move
	new_pos = perm_apply(move, pos)

	# hash the position
	new_hash = hash(new_pos)

	# check if this pos is original
	if hash_table.get(new_hash) == None:

		# this is a new pos: store the hash val as the key, and the path as the value
		new_path = path + [move]
		hash_table[new_hash] = new_path

		return new_pos, new_path

	return False


def checkForPath(forward_hash_table, reverse_hash_table, pos):

	hash_val = hash(pos)

	# search the hash tables with direct address lookup
	forward_path = forward_hash_table.get(hash_val)
	reverse_path = reverse_hash_table.get(hash_val)

	# check for the presence of the hash val in both tables
	if forward_path != None and reverse_path != None:
		print("found a path")

		# flip the path from the ending position to the connecting-position
		reverse_path.reverse()

		# invert the moves from the ending position to the connecting-position
		reverse_path = [perm_inverse(move) for move in reverse_path]

		# return the path
		return list(forward_path + reverse_path)

	return False


def shortest_path(start, end):

	# corner case for a 0 length path
	if start == end:
		print("It's already solved")
		return []

	"""
	Using 2-way BFS, finds the shortest path from start_position to
	end_position. Returns a list of moves. 
	You can use the rubik.quarter_twists move set.
	Each move can be applied using rubik.perm_apply
	"""

	# hash tables for storing all of the states found from each side
	s_table = {}
	s_table[hash(start)] = []
	e_table = {}
	e_table[hash(end)] = []

	# queues for storing the next-up permutations to explore
	s_queue = col.deque([[start, []]])
	e_queue = col.deque([[end, []]])

	while True:

		# loop through the items in this level of the tree, searching forward
		for n in range(len(s_queue)):

			# remove and store the first position in the queue
			cur_pos, cur_path = s_queue.popleft()

			# check if we've exceeded the largest (7+7) possible path, and therefore no path exists
			# this covers the "bad_path" corner case
			if len(cur_path) > 8:
				print("No path possible")
				return None

			# check all 6 possible moves
			for move in quarter_twists:

				# result is a tuple: (pos, path) or a Boolean: False
				result = tryPerm(cur_pos, move, cur_path, s_table)

				# if result is a legitamate novel permuation
				if result != False:

					# check for a path. path holds either a list or False
					path = checkForPath(s_table, e_table, result[0])
					
					# if a full path was found
					if path != False:

						return path

					# we've found a novel position, so add it to the queue to be searched in the next level
					s_queue.append(result)


		# loop through the items in this level of the tree, searching from the solved side
		for n in range(len(e_queue)):

			# remove and store the first position in the queue
			cur_pos, cur_path = e_queue.popleft()

			# check all 6 possible moves
			for move in quarter_twists:

				# result is a tuple: (pos, path) or a Boolean: False
				result = tryPerm(cur_pos, move, cur_path, e_table)

				# if result is a legitamate novel permuation
				if result != False:

					# check for a path. path holds either a list or False
					path = checkForPath(s_table, e_table, result[0])

					# if a full path was found
					if path != False:

						return path

					# we've found a novel position, so add it to the queue to be searched in the next level
					e_queue.append(result)