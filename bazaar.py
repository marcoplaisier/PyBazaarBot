import random


class Bazaar(object):
    """A bazaar is a place where bids and asks can be placed by agents. Each update, these orders are reconciled with
    each other. When a bid covers the ask, these are matched and a trade is successful.
    The bazaar publishes aggregate information about successful trades.
    """

    def __init__(self):
        self.bid_book = []
        self.ask_book = []

    def register_ask(self, ask):
        """Register an ask in the ask book which will be reconciled with the bid book when update is called.

        :param ask: the ask, a dictionary with the following keys: commodity, price, amount, seller
        """
        self.ask_book.append(ask)

    def register_bid(self, bid):
        self.bid_book.append(bid)

    def update(self):
        self.resolve_offers()

    def resolve_offers(self):
        random.shuffle(self.bid_book)
        random.shuffle(self.ask_book)

        self.bid_book.sort(key=lambda bid: bid['price'])
        self.ask_book.sort(key=lambda ask: ask['price'], reverse=True)
        
        while self.bid_book and self.ask_book:
            bid = self.bid_book.pop()
            ask = self.ask_book.pop()

            if bid['price'] >= ask['price']:
                remaining_bid, remaining_ask = self.resolve_offer(bid, ask)

                if remaining_ask:
                    self.ask_book.append(remaining_ask)
                if remaining_bid:
                    self.bid_book.append(remaining_bid)
            else:
                break

    #TODO: create simple statistics based on resolved trades

    def resolve_offer(self, bid, ask):
        trade_price = (bid['price'] + ask['price']) / 2.0
        trade_amount = min(bid['amount'], ask['amount'])

        ask['seller'].trade(bid['buyer'], bid['commodity'], trade_amount)
        bid['buyer'].pay(ask['seller'], trade_amount*trade_price)

        if bid['amount'] == trade_amount:
            bid = None
        else:
            bid['amount'] -= trade_amount

        if ask['amount'] == trade_amount:
            ask = None
        else:
            ask['amount'] -= trade_amount

        return bid, ask