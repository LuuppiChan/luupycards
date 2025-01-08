# SPDX-License-Identifier: GPL-2.0-or-later
import random
amount_of_pairs = 200

number_list = list(range(1, amount_of_pairs + 1))
random.shuffle(number_list)

while len(number_list):
    print(number_list)
    number_list.pop(0)

