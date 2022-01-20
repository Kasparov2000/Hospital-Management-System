# A function to calculate the minimum mark up. Since the prices are 2 decimal, 0.01 will require a minimum mark
# of 100% for the price to truly change. This function does that job

def minimum_mark_up(unit_cost):
    min_mark_up = round(0.01 / unit_cost, 2)

    if min_mark_up > 0.01:
        return min_mark_up
    else:
        return 0.01

