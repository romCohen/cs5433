from matplotlib import pyplot as plt

def calculate_profit(average_difficulty, hashrate_per_miner, num_miners, btc_usd_price, btc_per_block, months_to_mine):
    """ Calculate total net profit, in USD, for mining for a total duration of months_to_mine months.

        Args:
            average_difficulty (float): The average BTC difficulty, in BTC difficulty format.
            hashrate_per_miner (int): Hashrate of a single miner, in Hashes/s.
            num_miners (int): Number of miners used.
            btc_usd_price (int): Price of 1 Bitcoin in USD.
            btc_per_block (float): Miner revenue in BTC/block.
            months_to_mine (float): Number of months to run the miner.

        Returns:
            int: Total expected mining profit in USD, rounded down to the nearest integer.
    """

    epsilon = 1 # small epsilon to avoid divide by 0 errors

    total_hashrate = hashrate_per_miner*num_miners # hashes our pool can do per second (#hashes/sec)
    hashes_per_block = 2**32 * average_difficulty # expected hashes required to find a single block (#hashes)

    blocks_per_second = total_hashrate / (hashes_per_block + epsilon) # (1/sec)
    sec_to_mine = months_to_mine*3600*24*30  # n_seconds in timeframe
    usd_per_block = btc_per_block*btc_usd_price  # dollars_per_block


    return round(blocks_per_second*sec_to_mine*usd_per_block)


if __name__ == "__main__":

    # Read the input data and graph the results
    # you should not need to modify the below, if your solution passes the relevant test.
    months_to_mine = 2.0

    difficulties = {}
    block_numbers = []

    # import difficulties
    try:
        raw_difficulties = open("difficulty.csv").read().splitlines()
    except:
        raw_difficulties = open("data/difficulty.csv").read().splitlines()
    for difficulty_line in raw_difficulties:
        difficulty_line = difficulty_line.split(",")
        block_number = int(difficulty_line[0])
        difficulties[block_number] = float(difficulty_line[1])
        block_numbers.append(block_number)

    profitability = []
    block_numbers = block_numbers[:0-int(months_to_mine * 3 * 2016)] # exclude last several blocks, because no data is available for them yet
    for block_number in block_numbers:
        if block_number > 415000: # approximate S9 release date
            # use an s9 miner
            hashrate_per_miner = 14000000000000
        else:
            # use an s7 miner
            hashrate_per_miner = 4730000000000
        if block_number < 420000: # block 420k was a halvening
            # pre-adjustment; 25BTC+fees per block
            btc_per_block = 26.0
        else:
            # post-adjustment; 12.5BTC+(higher) fees per block
            btc_per_block = 14.0

        # calculate rough average of difficulty over overall mining period by sampling from difficulty adjustments
        total_difficulty = 0.0
        for diff_adjustment in range(int(2 * months_to_mine)):
            total_difficulty += difficulties[block_number + diff_adjustment * 2016]

        profitability.append(calculate_profit(total_difficulty / (2 * months_to_mine), hashrate_per_miner, 5, 10000, btc_per_block, 2.0))

    # generate plot
    plt.plot(block_numbers, profitability)
    plt.xlabel("Block Number")
    plt.ylabel("Estimated USD Profit generated in " + str(int(months_to_mine)) + " months of mining")
    plt.title("BTC Mining Profitability")
    plt.show()
