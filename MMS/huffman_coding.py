
import sys
import queue


class HuffmanCoding:
    """Huffman coding.

    Algorithm: (http://en.wikipedia.org/wiki/Huffman_coding)

    1. Create a leaf node for each symbol and add it to the priority queue.
    2. While there is more than one node in the queue:
        2.1. Remove the two nodes of highest priority (lowest probability) from the queue
        2.2. Create a new internal node with these two nodes as children and with probability equal to the sum of the two nodes' probabilities.
        2.3. Add the new node to the queue.
    3. The remaining node is the root node and the tree is complete.
    """

    class _TreeNode:
        """Internal tree node for building Huffman tree."""

        def __init__(self, node_priority, node_value=None, left=None, right=None):            
            self.left = left
            self.right = right

            self.priority = node_priority
            self.value = node_value

        def __lt__(self, other):
            if self.priority == other.priority:
                if self.value == None:
                    return True
                if other.value == None:
                    return False
                return self.value < other.value

            return self.priority < other.priority


    def averageBitsForEncoding(coding_schema):
        """Return an average bits need for coding."""

        sum_of_occurrences = 0
        sum_of_bits = 0

        for (char, occurences, coding) in coding_schema:
            sum_of_occurrences += occurences
            sum_of_bits += len(coding) * occurences

        return sum_of_bits / sum_of_occurrences

    
    def getCodingSchema(input):
        """Return a coding schema where coding shema is a list of tuple(char, number_of_occurences, coding_string)."""

        input_characters = [char for char in input]
        coding_schema = [(char, input_characters.count(char), '') for char in set(input_characters)]

        priority_queue = queue.PriorityQueue(len(coding_schema))

        for (char, occurences, coding_string) in coding_schema:
            priority_queue.put(HuffmanCoding._TreeNode(occurences, char))

        last_left_node = None
        last_right_node = None

        while priority_queue.qsize() > 1:

            left_node = priority_queue.get()
            right_node = priority_queue.get()
            
            new_node = HuffmanCoding._TreeNode(left_node.priority + right_node.priority)
            new_node.left = left_node
            new_node.right = right_node

            priority_queue.put(new_node)

            last_left_node = left_node
            last_right_node = right_node

        root_node = priority_queue.get()

        root_node.left_node = last_left_node
        root_node.right_node = last_right_node

        return HuffmanCoding._tree_to_coding_schema(root_node)


    def _tree_to_coding_schema(root_node):
        """Building coding schema from root tree node."""
        result = []
        HuffmanCoding._inorder_traversal(root_node, result, '')
        return result


    def _inorder_traversal(node, result, coding_string):
        if node == None:
            return

        HuffmanCoding._inorder_traversal(node.left, result, coding_string + '0')
         
        if node.value != None:
            result.append((node.value, node.priority, coding_string))

        HuffmanCoding._inorder_traversal(node.right, result, coding_string + '1')


def main():

    if len(sys.argv) != 2:
        print("I need input string to consume. :)")
        return

    coding_schema = HuffmanCoding.getCodingSchema(sys.argv[1])
    average_bits = HuffmanCoding.averageBitsForEncoding(coding_schema)

    print("Average bits needed:", average_bits)
    print("Compression factor:", 8 / average_bits)


if __name__ == "__main__":
    main() 