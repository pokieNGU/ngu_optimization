import numpy as np

# xp is total xp spent on a resource (such as energy):
# xp=1e6
# power = 3
# cap = 75000
# bars = 2
# ratio = (power, cap, bars)

ORDER_PRINT = ['NGU speed', 'Beard speed', 'Advanced Training']


class Ratio:
    def __init__(self, power, cap, bars):
        self.ratio_power = power
        self.ratio_cap = cap
        self.ratio_bars = bars
        self.xp_cost = self.xp_per_ratio()
        self.xp = None
        self.power = None
        self.cap = None
        self.bars = None

    def xp_per_ratio(self):
        return 150*self.ratio_power + self.ratio_cap/250 + self.ratio_bars*80

    def set_stats_with_xp(self, xp):
        self.xp = xp
        number_times_to_buy_ratio = xp/self.xp_cost
        self.power = number_times_to_buy_ratio*self.ratio_power
        self.cap = number_times_to_buy_ratio*self.ratio_cap
        self.bars = number_times_to_buy_ratio*self.ratio_bars

    def ngu_speed(self):
        if self.xp is None:
            raise ValueError('Call set_stats_with_xp() first.')
        return self.power*self.cap

    def beard_speed(self):
        if self.xp is None:
            raise ValueError('Call set_stats_with_xp() first.')
        return np.sqrt(self.power)*self.bars

    def at_speed(self):
        if self.xp is None:
            raise ValueError('Call set_stats_with_xp() first.')
        return np.sqrt(self.power)*self.cap

    def ratio_ngu_speed_per_total_xp(self):
        if self.xp is None:
            raise ValueError('Call set_stats_with_xp() first.')
        return self.ngu_speed()/self.xp

    def ratio_beard_speed_per_total_xp(self):
        if self.xp is None:
            raise ValueError('Call set_stats_with_xp() first.')
        return self.beard_speed()/self.xp

    def ratio_at_speed_per_total_xp(self):
        if self.xp is None:
            raise ValueError('Call set_stats_with_xp() first.')
        return self.at_speed()/self.xp

    def give_me_stats(self, xp, to_print=True):
        self.set_stats_with_xp(xp)
        if to_print:
            print('For the ratio of {} power : {} cap : {} bars and xp {} the stats are'.
                  format(self.ratio_power, self.ratio_cap, self.ratio_bars, self.xp))
            print('Ratio of NGU speed to xp is {}'.format(self.ratio_ngu_speed_per_total_xp()))
            print('Ratio of Beard speed to xp is {}'.format(self.ratio_beard_speed_per_total_xp()))
            print('Ratio of Advanced Training speed to xp is {}'.format(self.ratio_at_speed_per_total_xp()))
        return self.ratio_ngu_speed_per_total_xp(), self.ratio_beard_speed_per_total_xp(), self.ratio_at_speed_per_total_xp()


def compare_ratio_stats(new, old, weights=(1, 1, 1),):
    for i, x in enumerate(new):
        if x/old[i] < weights[i]:
            return False
    return True


def best_stats_ratio(new, old):
    out = []
    for i, x in enumerate(new):
        out.append(max(x, old[i]))
    return out



def print_compare_ratio_stats(new, old):
    for i, x in enumerate(new):
        print('{} : {}'.format([i], x/old[i]))


if __name__ == '__main__':
    meta_ratio = Ratio(3, 75000, 2)
    xp = 1e10
    meta_ratio.give_me_stats(xp)

    holy_number = 37500
    horatio1 = Ratio(1, holy_number, 2/3)
    horatio1.give_me_stats(xp)

    horatio2 = Ratio(7, 7*holy_number, 5)
    horatio2.give_me_stats(xp)

    horatio3 = Ratio(7, 7*holy_number, 6.4)
    horatio3.give_me_stats(xp)

    xp=1e6
    ratio1 = Ratio(1, holy_number, 2/3)
    print('This is the proposed ratio ')
    ratio1.give_me_stats(xp)
    print('\nThis is your ratio')
    ratio2 = meta_ratio
    ratio2.give_me_stats(xp)
    print('\nThese are the gains for the three speeds between the proposed ratio and your ratio')
    print_compare_ratio_stats(ratio1.give_me_stats(xp, to_print=False), ratio2.give_me_stats(xp, to_print=False))




    xp = 2.4e6
    meta_ratio = Ratio(3, 75000, 2)
    best_ratio = meta_ratio
    best_stats = best_ratio.give_me_stats(xp, to_print=False)
    for i in range(19000):
        power_bar_ratio = 0.1 + i/10000
        new_bar = 1/power_bar_ratio
        new_ratio = Ratio(1, holy_number, new_bar)
        new_stats = new_ratio.give_me_stats(xp, to_print=False)
        if compare_ratio_stats(new_stats, best_stats):
            best_ratio = new_ratio
            best_stats = new_stats
    best_ratio.give_me_stats(xp)

    power_bar_ratio = 7/6.4
    new_bar = 1/power_bar_ratio
    new_ratio = Ratio(1, holy_number, new_bar)
    new_stats = new_ratio.give_me_stats(xp)

    ########### WEIGHTED #######################
    xp = 2.4e6
    meta_ratio = Ratio(3, 75000, 2)
    best_ratio = meta_ratio
    best_stats = best_ratio.give_me_stats(xp, to_print=False)
    step_size = 1000
    for i in range(int(1.5*step_size)):
        power_bar_ratio = 0.5 + i / step_size
        new_bar = 1 / power_bar_ratio
        new_ratio = Ratio(1, holy_number, new_bar)
        new_stats = new_ratio.give_me_stats(xp, to_print=False)
        if compare_ratio_stats(new_stats, best_stats, weights=(1.1, 0.80, 0.9)):
            best_ratio = new_ratio
            best_stats = new_stats
    best_ratio.give_me_stats(xp)
    meta_ratio.give_me_stats(xp)
    print_compare_ratio_stats(best_stats, meta_ratio.give_me_stats(xp, to_print=False))

    ########### Big Loop #######################
    xp = 2.4e6
    meta_ratio = Ratio(3, 75000, 2)
    best_ratio = meta_ratio
    best_stats = best_ratio.give_me_stats(xp, to_print=False)
    step_size = 1000
    for i in range(int(1.5*step_size)):
        power_bar_ratio = 0.5 + i/step_size
        new_bar = 1 / power_bar_ratio

        for j in range(int(1*step_size)):
            cap_power_ratio = holy_number*(0.25 + i/step_size)
            new_cap = cap_power_ratio

            new_ratio = Ratio(1, new_cap, new_bar)
            new_stats = new_ratio.give_me_stats(xp, to_print=False)
            if compare_ratio_stats(new_stats, best_stats):
                best_ratio = new_ratio
                best_stats = best_stats_ratio
    best_ratio.give_me_stats(xp)
    meta_ratio.give_me_stats(xp)
    print_compare_ratio_stats(best_stats, meta_ratio.give_me_stats(xp, to_print=False))

# results
# For the ratio of 1 power : 34537.5 cap : 0.8539709649871904 bars and xp 2400000.0 the stats are
# Ratio of NGU speed to xp is 652321.7019678339
# Ratio of Beard speed to xp is 0.19657056749948826
# Ratio of Advanced Training speed to xp is 7949.9845467408995
# For the ratio of 3 power : 75000 cap : 2 bars and xp 2400000.0 the stats are
# Ratio of NGU speed to xp is 652095.1575896632
# Ratio of Beard speed to xp is 0.19549432527325747
# Ratio of Advanced Training speed to xp is 7331.037197747156
# [0] : 1.0003474099991911
# [1] : 1.0055052351249911
# [2] : 1.0844283465351872

    ########### Weighted Big Loop #######################
    xp = 2.4e6
    meta_ratio = Ratio(3, 75000, 2)
    best_ratio = meta_ratio
    best_stats = best_ratio.give_me_stats(xp, to_print=False)
    step_size = 1000
    for i in range(int(1.5*step_size)):
        power_bar_ratio = 0.5 + i/step_size
        new_bar = 1 / power_bar_ratio

        for j in range(int(1*step_size)):
            cap_power_ratio = holy_number*(0.25 + i/step_size)
            new_cap = cap_power_ratio

            new_ratio = Ratio(1, new_cap, new_bar)
            new_stats = new_ratio.give_me_stats(xp, to_print=False)
            if compare_ratio_stats(new_stats, best_stats, weights=(1.01, 0.85, 0.7)):
                best_stats = best_stats_ratio(new_stats, best_stats)
                best_ratio = new_ratio
    print('This is the best ratio found')
    best_ratio.give_me_stats(xp)
    print('\nThis is the meta ratio')
    meta_ratio.give_me_stats(xp)
    print('\nThese are the gains for the three speeds between best found ratio and meta ratio')
    print_compare_ratio_stats(best_ratio.give_me_stats(xp), meta_ratio.give_me_stats(xp, to_print=False))


    xp=1e6
    horatio1 = Ratio(1, holy_number, 2/3)
    print('This is the proposed ratio ')
    horatio1.give_me_stats(xp)
    print('\nThis is the meta ratio')
    meta_ratio.give_me_stats(xp)
    print('\nThese are the gains for the three speeds between the proposed ratio and meta ratio')
    print_compare_ratio_stats(horatio1.give_me_stats(xp, to_print=False), meta_ratio.give_me_stats(xp, to_print=False))

    xp=1e6
    horatio1 = Ratio(4, 90000, 3)
    print('This is the proposed ratio ')
    horatio1.give_me_stats(xp)
    print('\nThis is the meta ratio')
    meta_ratio.give_me_stats(xp)
    print('\nThese are the gains for the three speeds between the proposed ratio and meta ratio')
    print_compare_ratio_stats(horatio1.give_me_stats(xp, to_print=False), meta_ratio.give_me_stats(xp, to_print=False))

