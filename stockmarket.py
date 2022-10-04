"""CSC 161 Project: Milestone III

Hewan Kasaye
Lab Section MW 6:15-7:30pm
Fall 2021
"""


def test_data(filename, col, day):
    """A test function to query the data you loaded into your program.

    Args:
        filename: A string for the filename containing the stock data,
                  in CSV format.

        col: A string of either "date", "open", "high", "low", "close",
             "volume", or "adj_close" for the column of stock market data to
             look into.

             The string arguments MUST be LOWERCASE!

        day: An integer reflecting the absolute number of the day in the
             data to look up, e.g. day 1, 15, or 1200 is row 1, 15, or 1200
             in the file.

    Returns:
        A value selected for the stock on some particular day, in some
        column col. The returned value *must* be of the appropriate type,
        such as float, int or str.
    """
    opened = open(filename, 'r')
    order = opened.readlines()
    line = order[day].split(',')
    name = ["date", "open", "high", "low", "close", "adj_close", "volume"]
    column_name = name.index(col)
    if "." in line[column_name]:
        return float(line[column_name])
    elif "-" in line[column_name]:
        return str(line[column_name])
    else:
        return int(line[column_name])


def main():
    pass


if __name__ == '__main__':
    main()


def transact(funds, stocks, qty, price, buy=False, sell=False):
    """A bookkeeping function to help make stock transactions.

       Args:
           funds: An account balance, a float; it is a value of
           how much money you have,
                  currently.

           stocks: An int, representing the number of stock you currently own.

           qty: An int, representing how many stock you wish to buy or sell.

           price: An float reflecting a price of a single stock.

           buy: This option parameter, if set to true, will initiate a buy.

           sell: This option parameter, if set to true, will initiate a sell.

       Returns:
           Two values *must* be returned. The first (a float) is the new
           account balance (funds) as the transaction is completed. The second
           is the number of stock now owned (an int) after the transaction is
           complete.

           Error condition #1: If the `buy` and `sell` keyword parameters
           are both set to true, or both false. You *must* raise an
           ValueError exception with an appropriate error message since this
           is an ambiguous transaction.

           Error condition #2: If you buy, or sell without enough funds or
           stocks to sell, respectively.  You *must* raise an
           ValueError exception with an appropriate error message since this
           is an ambiguous transaction.
    """
    if buy is True and sell is False:
        costs = price * qty
        if costs > funds:
            raise ValueError(f"Sorry, Insufficient funds to purchase [qty] stock at ${price:0.2f}!")
        else:
            new_balance = funds - costs
            st_owned = int(stocks + qty)
            return new_balance, st_owned
    elif sell is True and buy is False:
        if qty <= stocks:
            gain = qty * price
            new_balance = gain + funds
            st_owned = int(stocks - qty)
            return new_balance, st_owned
        else:
            raise ValueError(f"Insufficient stock owned to sell {qty} stocks!")
    else:
        raise ValueError("Ambiguous transaction! Can't determine whether to buy or sell!")


def alg_moving_average(filename):
    """This function implements the moving average stock trading algorithm.

    The CSV stock data should be loaded into your program; use that data to
    make decisions using the moving average algorithm.

    Any bookkeeping setup from Milestone I should be called/used here.

    Algorithm:
    - Trading must start on day 21, taking the average of the previous 20 days.
    - You must buy shares if the current day price is 5%, or more, lower
      than the moving average.
    - You must sell shares if the current day price is 5%, or more, higher,
      than the moving average.
    - You must buy, or sell 10 stocks, or less per transaction.
    - You are free to choose which column of stock data to use (open, close,
      low, high, etc)
    - When your algorithm reaches the last day of data, have it sell all
      remaining stock. Your function will return the number of stocks you
      own (should be zero, at this point), and your cash balance.
    - Choose any stock price column you wish for a particular day you use
      (whether it's the current day's "open", "close", "high", etc)

    Args:
        A filename, as a string.

    Returns:
        Note: You *must* sell all your stock before returning.
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.

    Prints:
        Nothing.
    """
    fileopen = open(filename, 'r')
    readlines = fileopen.readlines()
    overallavg = 0
    cash_balance = 10000
    stocks_owned = 0
    for i in range(1, len(readlines)):
        if i < 21:
            line = readlines[i].split(',')
            openb, close = float(line[1]), float(line[4])
            dayavg = (openb + close) / 2
            overallavg = (overallavg * (i - 1) + dayavg) / i
        elif 21 <= i < len(readlines):
            line = readlines[i].split(',')
            openb, close = float(line[1]), float(line[4])
            high, low = float(line[2]), float(line[3])
            dayavg = (openb + close) / 2
            overallavg = (overallavg * (i - 1) + dayavg) / i
            if low < overallavg * 0.95:
                qty = cash_balance // low
                if qty < 10:
                    pass
                else:
                    cash_balance, stocks_owned = transact(cash_balance,
                                                          stocks_owned, qty,
                                                          low, buy=True)   
            elif high > overallavg * 1.05:
                if stocks_owned < 10:
                    pass
                else:
                    cash_balance, stocks_owned = transact(cash_balance, stocks_owned, stocks_owned, high,
                                                          sell=True)
        elif i == len(readlines):
            cash_balance, stocks_owned = transact(cash_balance, stocks_owned,
                                                  stocks_owned, high, sell=True)
    return stocks_owned, cash_balance


def alg_rsi(filename_1, filename_2):
    """This function implements the Relative Strength Index algorithm.

    Using the CSV stock data from two stock files that are loaded into your
    program, use that data to make decisions using the Relative Strength
    Index (RSI) algorithm.

    Algorithm:
        my avg gain and loss is from daily high
        then when buying, it uses the low of the day
        and high of the day when selling

    Arguments:
        filename_1 (str): A filename, as a string, for one set of stock
                          data for a first company.

        filename_2 (str): A filename, as a string, for one set of stock
                          data for a second company.

    Returns:
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.

    Prints:
        Nothing.
    """

    # Last thing to do, return two values: one for the number of stocks you
    # end up owning after the simulation, and the amount of money you have
    # after the simulation. Remember, all your stocks should be sold at the
    # end!

    cash_balance = 10000
    stocks1 = 0
    stocks2 = 0
    file1 = open(filename_1, 'r')
    file2 = open(filename_2, 'r')
    n1 = file1.readlines()
    n2 = file2.readlines()
    day = min(len(n1), len(n2))
    totalg1, totalg2, totall1, totall2 = 0, 0, 0, 0
    for i in range(1, day):
        l1 = n1[i].split(',')
        price1 = float(l1[2])
        l2 = n2[i].split(',')
        price2 = float(l2[2])
        if i <= 14:
            if i == 1:
                last1 = price1
                last2 = price2
                continue
            if price1 >= last1:
                gain1 = price1 - last1
                totalg1 += gain1
                last1 = price1
            elif price1 < last1:
                loss1 = last1 - price1
                totall1 += loss1
                last1 = price1
            if price2 >= last2:
                gain2 = price2 - last2
                totalg2 += gain2
                last2 = price2
            elif price2 < last2:
                loss2 = last2 - price2
                totall2 += loss2
                last2 = price2
        if price1 >= last1:
            gain1 = price1 - last1
            totalg1 += gain1
            last1 = price1
        elif price1 < last1:
            loss1 = last1 - price1
            totall1 += loss1
            last1 = price1
        if price2 >= last2:
            gain2 = price2 - last2
            totalg2 += gain2
            last2 = price2
        elif price2 < last2:
            loss2 = last2 - price2
            totall2 += loss2
            last2 = price2
        avgg1 = totalg1 / 14
        avgg2 = totalg2 / 14
        avgl1 = totall1 / 14
        avgl2 = totall2 / 14
        if avgl1 == 0:
            rsi1 = 100
        elif avgl2 == 0:
            rsi2 = 100
        rsi1 = 100 - (100 / (1 + (avgg1 / avgl1)))
        rsi2 = 100 - (100 / (1 + (avgg2 / avgl2)))
        if rsi1 <= 30:
            qty = cash_balance // price1
            if qty >= 10:
                cash_balance, stocks1 = transact(cash_balance, stocks1, qty,
                                                 price1, buy=True)
                # print(cash_balance, stocks_owned)
        elif rsi1 >= 70:
            if stocks1 >= 10:
                cash_balance, stocks1 = transact(cash_balance, stocks1,
                                                 stocks1, price1, sell=True)
                # print(cash_balance, stocks_owned)\
        if rsi2 <= 30:
            qty = cash_balance // price2
            if qty >= 10:
                cash_balance, stocks2 = transact(cash_balance, stocks2, qty,
                                                 price2, buy=True)
                # print(cash_balance, stocks_owned)
        elif rsi2 >= 70:
            if stocks2 >= 10:
                cash_balance, stocks2 = transact(cash_balance, stocks2,
                                                 stocks2, price2, sell=True)
        
        """
        if rsi2 < 30:
            qty = cash_balance // price2
            if qty >= 10:
                cash_balance, stocks_owned = \
                transact(cash_balance, stocks_owned, qty, price2, buy=True)
                print(cash_balance, stocks_owned)
        elif rsi2 > 70:
            if stocks_owned >= 10:
                cash_balance, stocks_owned = \
                transact(cash_balance, stocks_owned, stocks_owned,
                         price1, sell=True)
                print(cash_balance, stocks_owned)
        """

    cash_balance, stocks1 = transact(cash_balance, stocks1, stocks1, price1,
                                     sell=True)
    cash_balance, stocks2 = transact(cash_balance, stocks2, stocks2, price2,
                                     sell=True)
    stocks_owned = stocks1 + stocks2
    # print(cash_balance, stocks_owned)
    return stocks_owned, cash_balance

    
# Don't forget the required "__main__" check!
def main():
    # My testing will use AAPL.csv or MSFT.csv
    stock_file_1 = input("Enter a filename for stock data (in CSV format): ")
    filename_1 = "MSFT.csv"
    # Call your moving average algorithm, with the filename to open.
    alg1_stocks, alg1_balance = alg_moving_average(filename_1)

    # Print results of the moving average algorithm, returned above:
    print("The results for algorithm 1 are: cash balance with {0:0.2f}"
          .format(alg1_balance), "stock balance with", alg1_stocks)

    # Now, call your RSI algorithm!
    stock_file_2 = input("Enter another filename for second stock data "
                         " file (in CSV format): ")
    alg2_stocks, alg2_balance = alg_rsi(stock_file_1, stock_file_2)

    # Print results of your algorithm, returned above:
    print("\nThe results for algorithm 2 are: cash balance with {0:0.2f}"
          .format(alg2_balance), "and with stock balance", alg2_stocks)


if __name__ == '__main__':
    main()
