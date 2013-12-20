
import sys
from functools import reduce


class ShannonFanoCoding:
    """ Shannon-Fano coding.

        More on http://en.wikipedia.org/wiki/Shannon%E2%80%93Fano_coding
    """
 
    def averageBitsForEncoding(codingSchema):
        """Return an average bits need for encoding."""

        sum_of_occurrences = 0
        sum_of_bits = 0

        for (char, occurences, encoding) in codingSchema:
            sum_of_occurrences += occurences
            sum_of_bits += len(encoding) * occurences

        return sum_of_bits / sum_of_occurrences


    def getCodingScheme(input):
        """Return a coding schema where coding shema is a list of tuple(char, number_of_occurences, encoding_schema)."""

        # Break input into chars
        input_char_list = set([char for char in input])

        # Count occurences and sort them out
        occurrences_list = [(char, input.count(char), '') for char in input_char_list]
        occurrences_list = sorted(occurrences_list, key=lambda occurrence: occurrence[1], reverse=True)

        # occurences_list is list of tuple (char, number_of_occurences, encoding)
        # ie. (input string is 'hello')
        #  occurences_list = [('l', 2, ''), ('h', 1, ''), ('e', 1, ''), ('o', 1, '')]

        return ShannonFanoCoding._process_partials(occurrences_list, len(occurrences_list))


    # Processes occurrences_list and adds encoding shcema to every item
    def _process_partials(occurrences_list, occurrences_list_len):
        if occurrences_list_len == 1:
            return occurrences_list

        # Get index where both parts have approx. occurences count
        half = ShannonFanoCoding._get_middle(occurrences_list, occurrences_list_len)

        # Add encoding values for both left and right part
        left_part = [(char, occurrences, encoding + '0') for (char, occurrences, encoding) in occurrences_list[:half]]
        right_part = [(char, occurrences, encoding + '1') for (char, occurrences, encoding) in occurrences_list[half:]]

        left_part = ShannonFanoCoding._process_partials(left_part, half)
        right_part = ShannonFanoCoding._process_partials(right_part, occurrences_list_len - half)

        return left_part + right_part

    # Sum two occurences; Used in reduce function
    def _sum_of_occurrences(x, y):
        if type(x) == int:
            return x + y[1]
        return x[1] + y[1]

    # Returns index where both parts have approx. occurences count
    def _get_middle(occurrences_list, occurrences_list_len):

        min_difference_index = None
        min_difference = None

        for i in range(1, occurrences_list_len):

            # Sum of occurences
            left_part_occurrences = reduce(ShannonFanoCoding._sum_of_occurrences, occurrences_list[:i])
            right_part_occurrences = reduce(ShannonFanoCoding._sum_of_occurrences, occurrences_list[i:])

            left_part_occurrences = ShannonFanoCoding._sum_of_occurrences(left_part_occurrences, [0, 0])
            right_part_occurrences = ShannonFanoCoding._sum_of_occurrences(right_part_occurrences, [0, 0])

            difference = abs(right_part_occurrences - left_part_occurrences)

            if min_difference == None:
                min_difference_index = i
                min_difference = difference
            else:
                if min_difference > difference:
                    min_difference_index = i
                    min_difference = difference

        return min_difference_index


def main():

    if len(sys.argv) != 2:
        print("I need input string to consume. :)")
        return

    codingSchema = ShannonFanoCoding.getCodingScheme(sys.argv[1])
    averageBits = ShannonFanoCoding.averageBitsForEncoding(codingSchema)

    print("Average bits needed:", averageBits)
    print("Compression factor:", 8 / averageBits)


if __name__ == "__main__":
    main()