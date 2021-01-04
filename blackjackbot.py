import datetime
import random
import typing
from collections import defaultdict

USE_EMOJI_TYPE = "Discord"
NB_DECKS = 1
RESET_HOUR = 8 #UTC ! [0;24]
BASE_BET = 2.0
MAX_HANDS_SPLIT = 2
CAN_HIT_AFTER_SPLIT_A = True
CAN_SPLIT_UNSUITED_10S = False
CAN_DOUBLE_AFTER_SPLIT = True
ONLY_DOUBLE_ON_HARD_9 = False
ONLY_DOUBLE_ON_HARD_10_11 = False
STACK_DOUBLES = True
SURRENDER_OPTION = True
BANK_STAND_ON_A6 = False
A10_IS_BLACKJACK = False
NO_TIES_ON_BLACKJACKS = True
INSURANCE_OPTION = True
INSURANCE_WITH_BANK_10S = False
PLAYER_MAX_BUSTS_TODAY = 3
MAX_DEALS_TODAY = 50
CARDS_IN_DECK_TO_RESHUFFLE = 0


def twoFigsPlusAce(player_hand, bank_hand):  #Pays 5 to 1
    if (len(player_hand.cards) == 3
            and player_hand.getTotal() == 21
            and str(player_hand.cards[0]) != '10'
            and str(player_hand.cards[1]) != '10'
            and str(player_hand.cards[2]) == 'A'):
        return 5 * player_hand.bet
    return 0


def tripleSevens(player_hand, bank_hand):  #Pays 7 to 1
    if (len(player_hand.cards) == 3
            and (str(player_hand.cards[0]) == str(player_hand.cards[1]) == str(player_hand.cards[2]) == '7')):
        return 7 * player_hand.bet
    return 0


def manyCards(player_hand, bank_hand):  #Pays 1 per bonus card from 5 onwards
    return max(player_hand.bet * (len(player_hand.cards) - 4), 0)


def bothTwentySuited(player_hand, bank_hand):  #1 time push to the next bet
    if (len(player_hand.cards) == 2
            and (str(player_hand.cards[0]) == str(player_hand.cards[1]))
            and player_hand.getTotal() == 20
            and len(bank_hand.cards) == 2
            and (str(bank_hand.cards[0]) == str(bank_hand.cards[1]))
            and bank_hand.getTotal() == 20):
        return player_hand.bet
    return 0


WIN_BONUSES_LIST = [twoFigsPlusAce, tripleSevens, manyCards]
PUSH_BONUSES_LIST = [bothTwentySuited]

#Source = https://wizardofodds.com/games/blackjack/strategy/4-decks/
strategy_bank_indexes: list = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
strategy_stand_on_soft_17: dict = {
    "Hard": {
        4: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        5: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        6: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        7: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        8: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        9: ['H', 'Dh', 'Dh', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        10: ['Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'H', 'H'],
        11: ['Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'H'],
        12: ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        13: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        14: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        15: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'Rh', 'H'],
        16: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'Rh', 'Rh', 'Rh'],
        17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        18: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        21: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
    },
    "Soft": {
        13: ['H', 'H', 'H', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        14: ['H', 'H', 'H', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        15: ['H', 'H', 'Dh', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        16: ['H', 'H', 'Dh', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        17: ['H', 'Dh', 'Dh', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        18: ['S', 'Ds', 'Ds', 'Ds', 'Ds', 'S', 'S', 'H', 'H', 'H'],
        19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        21: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
    },
    "Pair": {
        2: ['Ph', 'Ph', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
        3: ['Ph', 'Ph', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
        4: ['H', 'H', 'H', 'Ph', 'Ph', 'H', 'H', 'H', 'H', 'H'],
        5: ['Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'H', 'H'],
        6: ['Ph', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],
        7: ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
        8: ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        9: ['P', 'P', 'P', 'P', 'P', 'S', 'P', 'P', 'S', 'S'],
        10: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        11: ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
    }
}

strategy_hit_on_soft_17: dict = {
    "Hard": {
        4: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        5: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        6: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        7: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        8: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        9: ['H', 'Dh', 'Dh', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        10: ['Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'H', 'H'],
        11: ['Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh'],
        12: ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        13: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        14: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        15: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'Rh', 'Rh'],
        16: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'Rh', 'Rh', 'Rh'],
        17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'Rs'],
        18: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        21: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
    },
    "Soft": {
        13: ['H', 'H', 'H', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        14: ['H', 'H', 'H', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        15: ['H', 'H', 'Dh', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        16: ['H', 'H', 'Dh', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        17: ['H', 'Dh', 'Dh', 'Dh', 'Dh', 'H', 'H', 'H', 'H', 'H'],
        18: ['Ds', 'Ds', 'Ds', 'Ds', 'Ds', 'S', 'S', 'H', 'H', 'H'],
        19: ['S', 'S', 'S', 'S', 'Ds', 'S', 'S', 'S', 'S', 'S'],
        20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        21: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
    },
    "Pair": {
        2: ['Ph', 'Ph', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
        3: ['Ph', 'Ph', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
        4: ['H', 'H', 'H', 'Ph', 'Ph', 'H', 'H', 'H', 'H', 'H'],
        5: ['Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'Dh', 'H', 'H'],
        6: ['Ph', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],
        7: ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
        8: ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'Rp'],
        9: ['P', 'P', 'P', 'P', 'P', 'S', 'P', 'P', 'S', 'S'],
        10: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        11: ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
    }
}

list_emoji_dict: dict= {
    "Unicode": {
        'A': '\u0041',
        '1': '\u0031',
        '2': '\u0032',
        '3': '\u0033',
        '4': '\u0034',
        '5': '\u0035',
        '6': '\u0036',
        '7': '\u0037',
        '8': '\u0038',
        '9': '\u0039',
        '10': '\u0031'+'\u0030',
        'J': '\u004A',
        'Q': '\u0051',
        'K': '\u004B',
        '?': '\u003F',
        "Heart": '\u2665',
        "Spade": '\u2660',
        "Diamond": '\u2666',
        "Club": '\u2663'
    },
    "Discord": {
        'A': ":regional_indicator_a:",
        '1': ":one:",
        '2': ":two:",
        '3': ":three:",
        '4': ":four:",
        '5': ":five:",
        '6': ":six:",
        '7': ":seven:",
        '8': ":eight:",
        '9': ":nine:",
        '10': ":ten:",
        'J': ":regional_indicator_j:",
        'Q': ":regional_indicator_q:",
        'K': ":regional_indicator_k:",
        '?': ":question:",
        "Heart": ":hearts:",
        "Spade": ":spades:",
        "Diamond": ":diamonds:",
        "Club": ":clubs:"
    }
}
list_values_dict: dict = {
    'A': 11,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10
}
###list_real_values: list = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
list_ranks: list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
list_suits: list = ["Heart", "Spade", "Diamond", "Club"]


class Player:
    def __init__(self, id_player: int, name: str, deals: int = 0, current_bet: int = BASE_BET, points: int = 0,
                 push_points: int = 0, auto_mode: bool = False):
        self.id: int = id_player  #Identifiant Discord
        self.name: str = name  #Nom du joueur (nick lors de l'inscription)
        self.deals: int = deals  #Participation aux parties d'aujourd'hui
        self.busts: int = 0  #Parties terminées en Bust aujourd'hui
        self.current_bet: int = current_bet #La mise du joueur au début de chaque Deal, modifiable
        self.points: int = points  #Cagnotte de points, réinitialisée chaque jour
        self.push_points: int = push_points  #Nombre de points remis en jeu (par Push) aujourd'hui, remis à zéro chaque jour
        self.auto_mode: bool = auto_mode  #Mode automatique
        self.days_into_auto_mode: int = 0  #Jours restants pour mode automatique. Valeur négative = infini
        self.deals_played: dict = {}  #Historique de participations. Forme : {Date: nb_deals}
        self.points_gained: dict = {}  #Historique de points gagnés. Forme : {Date: nb_points}
        #TODO merge 'deals_played' and 'points_gained' into 'history' ? {Date: Tuple(nb_deals, nb_points)}

    def canPlay(self) -> bool:
        return ((self.points + self.push_points) >= BASE_BET
                and self.busts < PLAYER_MAX_BUSTS_TODAY
                and self.deals < MAX_DEALS_TODAY)

    def saveTodayStatus(self):
        if self.deals > 0:
            self.deals_played[datetime.datetime.today()] = self.deals
            self.points_gained[datetime.datetime.today()] = self.points
            self.deals = 0
            self.busts = 0
            self.points = 0
            self.push_points = 0

        if self.days_into_auto_mode > 0:
            self.days_into_auto_mode -= 1
            self.auto_mode = (self.days_into_auto_mode != 0)


class Card:
    def __init__(self, rank: str, suit: str, hidden: bool = False):
        if not(rank in list_ranks) :
            raise TypeError("Rank provided ("+rank+") not in list_ranks")
        if not(suit in list_suits) :
            raise TypeError("Suit provided ("+suit+") not in list_suit")
        self.rank: str = rank
        self.suit: str = suit
        self.hidden: bool = hidden

    def getValue(self) -> int:
        if not self.hidden:
            return list_values_dict[self.rank]
            ###return list_real_values[list_values.index(self.value)]
        return 0

    def toEmoji(self, thing) -> any:
        return list_emoji_dict[USE_EMOJI_TYPE][thing]

    def display(self) -> str:
        if not self.hidden:
            return self.toEmoji(self.rank) + self.toEmoji(self.suit)
        return self.toEmoji('?') + self.toEmoji('?')

    def __str__(self) -> str:
        return self.rank


class Hand:
    def __init__(self, player_id: int, cards: typing.List[Card], bet: typing.Union[int, float], split_level: int = 0,
                 insurance: bool = False):
        self.player_id: int = player_id  #0 pour la banque
        self.cards: list = list(cards)
        self.bet: float = float(bet)
        self.split_level: int = split_level
        self.insurance: bool = insurance
        self.nb_aces: int = len(list(filter(lambda a: str(a) == 'A', self.cards)))
        self.total: int = 0
        for c in self.cards:
            self.total += c.getValue()

    def getTotal(self) -> int:
        """ #DEPRECATED, solution plus complexe
        sum = 0
        for c in self.cards:
            value = c.getValue()
            if isinstance(value, list):
                sum = max(filter(lambda c:c+sum<=21+(10*self.nb_aces), value), default=min(value))
            if isinstance(value, int):
                sum += value
        """
        h_sum = self.total
        aces = self.nb_aces
        while (h_sum > 21) and (aces > 0):
            h_sum -= 10
            aces -= 1
        return h_sum

    def addCard(self, card: Card):
        self.cards.append(card)
        if not card.hidden:
            self.nb_aces += 1 if str(card) == 'A' else 0
            self.total += card.getValue()

    def takeLastCard(self) -> Card:
        card = self.cards.pop(-1)
        if not card.hidden:
            self.nb_aces -= 1 if str(card) == 'A' else 0
            self.total -= card.getValue()
        return card

    def reveal(self, c: int):
        try:
            if self.cards[c].hidden:
                self.cards[c].hidden = False
                self.nb_aces += 1 if str(self.cards[c]) == 'A' else 0
                self.total += self.cards[c].getValue()
        except IndexError:
            print("IndexError on reveal")

    def revealAll(self):
        for c, card in enumerate(self.cards):
            self.reveal(c)

    def hide(self, c: int):
        try:
            if not (self.cards[c].hidden):
                self.cards[c].hidden = True
                self.nb_aces -= 1 if str(self.cards[c]) == 'A' else 0
                self.total -= self.cards[c].getValue()
        except IndexError:
            print("IndexError on hide")

    def hideAll(self):
        for c, card in enumerate(self.cards):
            self.hide(c)

    def canDouble(self) -> bool:
        tot = self.getTotal()
        if self.split_level > 0 and not CAN_DOUBLE_AFTER_SPLIT:
            return False
        if ONLY_DOUBLE_ON_HARD_9 and ONLY_DOUBLE_ON_HARD_10_11:
            return (tot >= 9) and (tot <= 11)
        if ONLY_DOUBLE_ON_HARD_9:
            return (tot == 9)
        if ONLY_DOUBLE_ON_HARD_10_11:
            return (tot == 10) or (tot == 11)
        return True

    def canSplit(self) -> bool:
        if CAN_SPLIT_UNSUITED_10S:
            return (len(self.cards) == 2
                    and self.cards[0].getValue() == self.cards[1].getValue()
                    and self.split_level + 1 < MAX_HANDS_SPLIT)
        return (len(self.cards) == 2
                and str(self.cards[0]) == str(self.cards[1])
                and self.split_level + 1 < MAX_HANDS_SPLIT)

    def canSurrender(self) -> bool:
        return len(self.cards) == 2 and self.split_level == 0 and SURRENDER_OPTION

    def isBlackJack(self) -> bool:
        if len(self.cards) == 2 and self.total == 21:
            return A10_IS_BLACKJACK or (str(self.cards[0]) != '10' and str(self.cards[1]) != '10')
        return False

    def display(self) -> str:
        res = ""
        for card in self.cards:
            res += card.display() + " -- "
        res += "\n" + str(self.getTotal())
        return res


class Deal:

    """
    nb_players: int
    players: dict(Player), normalement indexes uniques
    players_hand: list(Hand)
    bank_hand: Hand
    """
    def __init__(self, *players: Player):
        self.nb_players: int = len(players)
        self.players: list = [] #Player list
        self.players_hand: dict = {} #{player_id : Hand | list(Hand)} 
        for player in players:
            self.players.append(player)
            self.players_hand[player.id] = [Hand(player.id, [], BASE_BET)]
        self.bank_hand: Hand = Hand(0, [], BASE_BET)
        self.deck: typing.List[Card] = self.generateDeck()

    def generateDeck(self, nb_decks: int=1) -> typing.List[Card]:
        res = []
        for i in range(nb_decks):
            for r in list_ranks:
                for s in list_suits:
                    res.append(Card(r, s))
        random.shuffle(res)
        return res

    def reshuffleDeck(self):
        self.deck.clear()
        self.deck = self.generateDeck()

    def drawCard(self, to_hand: Hand, is_hidden: bool=False):
        new_card = self.deck.pop(0)
        new_card.hidden = is_hidden
        if len(self.deck) <= CARDS_IN_DECK_TO_RESHUFFLE:
            self.reshuffleDeck()
        to_hand.addCard(new_card)

    def newDeal(self):
        # re-init
        self.players_hand.clear()
        self.bank_hand = None
        for player in self.players:
            #TODO take custom bets ?
            self.players_hand = [Hand(player.id, [], BASE_BET)]
        self.bank_hand = Hand(0, [], BASE_BET)

        for p_hand in self.players_hand:
            self.drawCard(p_hand)
        self.drawCard(self.bank_hand)
        for p_hand in self.players_hand:
            self.drawCard(p_hand)
        self.drawCard(self.bank_hand, True)

    def standCommand(self, hand: Hand) -> typing.Tuple[int, bool, bool]:  #(new_total, finished, busted)
        return (hand.getTotal(), True, False)

    def hitCommand(self, hand: Hand) -> typing.Tuple[int, bool, bool]:  #(new_total, finished, busted)
        self.drawCard(hand, False)
        new_total = hand.getTotal()
        return (new_total, new_total >= 21, new_total > 21)
        #Automatically finished when score is 21 or more
        #Automatically busted when score is 22 or more

    def doubleCommand(self, hand: Hand, bonus_bet: int=BASE_BET) -> typing.Tuple[int, bool, bool]:  #(new_total, finished, busted)
        hand.bet += bonus_bet
        (new_total, finished, busted) = self.hitCommand(hand)
        return (new_total, True, busted)

    def splitCommand(self, hands: typing.List[Hand], i: int) -> Card:
        new_card = hands[i].takeLastCard()
        hands[i].split_level += 1
        hands.append(Hand(hands[i].player_id, [new_card], BASE_BET, hands[i].split_level, hands[i].insurance))
        return new_card

    def surrenderCommand(self, hand: Hand) -> typing.Tuple[int, bool, bool]:  #(new_total, finished, busted)
        hand.bet /= 2
        return (hand.getTotal(), True, True)  #TODO quelle situation ? Renvoyer une main busted ou modifier son bet ?

    def hintCommand(self, player_hand: Hand, bank_hand: Hand) -> str:
        #Renvoie la stratégie conseillé par rapport à la cheatsheet
        if player_hand.canSplit():
            h_type = "Pair"
            player_value = player_hand.cards[0].getValue()
        elif (str(player_hand.cards[0]) == 'A' or str(player_hand.cards[1]) == 'A'
              and ((str(player_hand.cards[0]) == 'A' and str(player_hand.cards[1]) == 'A')
                   or player_hand.total == player_hand.getTotal())):
            #La main de début contient un As non compensé
            #ou deux As ne pouvant pas être splittés
            h_type = "Soft"
            player_value = player_hand.getTotal()
        else:
            h_type = "Hard"
            player_value = player_hand.getTotal()
        bank_value = strategy_bank_indexes.index(bank_hand.cards[0].getValue())
        if BANK_STAND_ON_A6:
            strat = strategy_stand_on_soft_17[h_type][player_value][bank_value]
        else:
            strat = strategy_hit_on_soft_17[h_type][player_value][bank_value]

        if strat == 'H':
            return "Hit"
        elif strat == 'S':
            return "Stand"
        elif strat == 'Dh':
            return "Double" if player_hand.canDouble() else "Hit"
        elif strat == 'Ds':
            return "Double" if player_hand.canDouble() else "Stand"
        elif strat == 'P':
            return "Split"
        elif strat == 'Ph':
            return "Split" if CAN_DOUBLE_AFTER_SPLIT else "Hit"
        elif strat == 'Rh':
            return "Surrender" if player_hand.canSurrender() else "Hit"
        elif strat == 'Rs':
            return "Surrender" if player_hand.canSurrender() else "Stand"
        elif strat == 'Rp':
            return "Surrender" if player_hand.canSurrender() else "Split"
        else:
            return "Error"

    def autoCommand(self, player_hand: Hand, bank_hand: Hand, verbose_mode: bool=False) -> typing.Tuple[int, bool, bool]:
        command_to_play = self.hintCommand(player_hand, bank_hand)
        if command_to_play == "Hit":
            return self.hitCommand(player_hand)
        elif command_to_play == "Stand":
            return self.standCommand(player_hand)
        elif command_to_play == "Double":
            return self.doubleCommand(player_hand)
        elif command_to_play == "Split":
            new_card = self.splitCommand([player_hand], 0)
            (new_total, finished, busted) = self.hitCommand(player_hand)
            if str(new_card) == 'A' and not CAN_HIT_AFTER_SPLIT_A:
                finished = True
            return (new_total, finished, busted)
            #TODO juste ou faux ???
        elif command_to_play == "Surrender":
            return self.surrenderCommand(player_hand)
        else:
            pass  #Error
        #Note : La version automatique ne prend jamais l'assurance

    def insuranceCommand(self, hand: Hand):
        hand.insurance = True

    def display(self) -> str:
        res = "DEAL :\n"
        for p in self.players:
            res += str(self.players_hand.keys()) + str(self.players_hand[p].display()) + "\n"
        res += "Bank : " + self.bank_hand.display()
        return res


class MainGame:
    player = {}
    player_ready = {}
    deal = Deal(Player(1, "Patrick"), Player(2, "Francis"))

    got_hint = False

    def newPlayer(self):
        pass
        

    def legalCommands(self, player_hand: Hand, got_hint: bool=got_hint) -> list:
        cmds = ["Auto", "Stand", "Hit"]
        if player_hand.canDouble():
            cmds.append("Double")
        if player_hand.canSplit():
            cmds.append("Split")
        if player_hand.canSurrender():
            cmds.append("Surrender")
        if not got_hint:
            cmds.append("Hint")
        else:
            cmds.append("PlayHint")
        return cmds

    def calculateWin(self, player: Player, player_hand: Hand, bank_hand: Hand):
        score = player_hand.bet
        for bonus in WIN_BONUSES_LIST:
            score += bonus(player_hand, bank_hand)  #call function
        if player_hand.isBlackJack():
            score *= 1.5
        player.points += score + player.push_points
        player.push_points = 0

    def calculatePush(self, player: Player, player_hand: Hand, bank_hand: Hand):
        push_score = player_hand.bet
        for bonus in PUSH_BONUSES_LIST:
            push_score += bonus(player_hand, bank_hand)  #call function
        if player_hand.isBlackJack() and bank_hand.isBlackJack():
            push_score *= 1.5
        player.push_points += push_score

    def calculateLose(self, player: Player, player_hand: Hand, bank_hand: Hand):
        score = player_hand.bet
        if bank_hand.isBlackJack():
            score *= 1.5
        player.points -= min(player.points, score)
        player.push_points = 0

    def calculateBust(self, player: Player, player_hand: Hand, bank_hand: Hand):
        #TODO La logique du Bust prend en compte les BlackJack ?
        player.points -= min(player.points, player_hand.bet)

    def turn(self, deal: Deal=None, got_hint: bool=got_hint):
        if deal is None:
            deal = self.deal
        deal.newDeal()
        if (str(deal.bank_hand.cards[0]) == 'A') and INSURANCE_OPTION:
            for p in deal.players_hand:
                p.insurance = input("Take insurance ? (True/False):")  #True or False

        for p, p_hand in enumerate(deal.players_hand):  #Un joueur
            (new_total, finished, busted) = (p_hand.getTotal(), p_hand.getTotal() >= 21, p_hand.getTotal() > 21)
            if (len(p_hand.cards) == 1 and p_hand.cards[0] == 'A'
                    and p_hand.split_level > 0 and not CAN_HIT_AFTER_SPLIT_A):
                (new_total, finished, busted) = deal.hitCommand(p_hand)
                finished = True
            while not (finished) or not (busted):
                print(self.legalCommands(p_hand))
                command_to_play = "Auto" if deal.players[p_hand.id].auto_mode else input("Waiting for command:")
                #TODO contrôle de l'input : est-ce que cette commande est légale ?
                if command_to_play in self.legalCommands(p_hand):
                    if command_to_play == "Hit":
                        (new_total, finished, busted) = deal.hitCommand(p_hand)
                        got_hint = False
                    elif command_to_play == "Stand":
                        (new_total, finished, busted) = deal.standCommand(p_hand)
                        got_hint = False
                    elif command_to_play == "Double":
                        (new_total, finished, busted) = deal.doubleCommand(p_hand)
                        got_hint = False
                    elif command_to_play == "Split":
                        new_card = deal.splitCommand(p_hand, p)
                        got_hint = False
                        (new_total, finished, busted) = deal.hitCommand(p_hand)
                        if str(new_card) == 'A' and not CAN_HIT_AFTER_SPLIT_A:
                            #faire un seul hit sur cette main et la nouvelle
                            finished = True
                    elif command_to_play == "Surrender":
                        (new_total, finished, busted) = deal.surrenderCommand(p_hand)
                        got_hint = False
                    elif command_to_play == "Hint":
                        if got_hint:  #Hint becomes PlayHint legally
                            (new_total, finished, busted) = deal.autoCommand(p_hand, deal.bank_hand)
                            got_hint = False
                        else:
                            print(deal.hintCommand(p_hand, deal.bank_hand))
                            got_hint = True
                    elif command_to_play == "PlayHint": #Like auto_mode for ONE card
                        (new_total, finished, busted) = deal.autoCommand(p_hand, deal.bank_hand, verbose_mode=True)
                        got_hint = False
                    elif command_to_play == "Auto":
                        while not (finished) or not (busted):
                            (new_total, finished, busted) = deal.autoCommand(p_hand, deal.bank_hand, verbose_mode=True)
                        got_hint = False
                else:
                    print("Not legal command")

        #tour de la banque
        deal.bank_hand.revealAll()
        if (deal.bank_hand.getTotal() == 17 and deal.bank_hand.nb_aces > 0
                and len(deal.bank_hand.cards) == 2 and BANK_STAND_ON_A6):
            deal.standCommand(deal.bank_hand)
        else:
            while deal.bank_hand.getTotal() < 17:
                deal.hitCommand(deal.bank_hand)
            deal.standCommand(deal.bank_hand)
        #fin du tour : contrôle des scores
        b_total = deal.bank_hand.getTotal()
        if b_total > 21:
            for p in deal.players_hand:
                self.calculateWin(deal.players[p.player_id], p, deal.bank_hand)
        else:
            for p in deal.players_hand:
                if deal.bank_hand.isBlackJack():
                    #TODO calcul des assurances ici
                    pass

                p_total = p.getTotal()
                if p_total > 21:
                    self.calculateLose(deal.players[p.player_id], p, deal.bank_hand)
                elif p_total > b_total:
                    self.calculateWin(deal.players[p.player_id], p, deal.bank_hand)
                elif p_total == b_total:
                    if NO_TIES_ON_BLACKJACKS:
                        self.calculateLose(deal.players[p.player_id], p, deal.bank_hand)
                    else:
                        self.calculatePush(deal.players[p.player_id], p, deal.bank_hand)
                else:
                    self.calculateLose(deal.players[p.player_id], p, deal.bank_hand)


"""
Données d'une carte
class Card:
value: Enum(A,2,3,4,5,6,7,8,9,10,J,Q,K)
color: Enum(Heart,Spade,Diamond,Club)
__str__: toEmoji(value)+toEmoji(color)

Deck de cartes
deck = list[Card, Card, Card.....]
^ 52 cartes, tirage sans remise
Remélanger le deck à chaque fois que le nombre de cartes passe en dessous de 20???

Système de points et de parties
Player
points

Deal
nbplayers: int
players: dict(Hand) ou dict(list(Hand))
bank: Hand
^ XXXXXXXXXX pour players: le dictionnaire a des index impairs pour chaque joueur (1,3,5...), lorsqu'une main est séparée, celle-ci prend l'index+1. Ainsi aucun décalage ne se fait dans le dict.
Selon l'option (maxSepares = 2 ou maxSepares > 2 : on utilise dict(Hand) ou dict(list(Hand)).

Hand
cards: list(Card)


Tableau de gains :
Win : +x points selon le nombre de cartes de ce joueur + de la banque.
Lose: -x points selon le nombre de cartes de ce joueur + de la banque.
Push: x points sont mis en attente selon le nombre de cartes de ce joueur + de la banque, remis en jeu à la prochaine manche de ce joueur.
Bust: -x points selon le nombre de cartes de ce joueur. (la différence avec le Lose est que le joueur perd IMMEDIATEMENT les points)
Win w/BlackJack: +1+x points selon le nombre de cartes de ce joueur + de la banque.
Lose VSBlackJack: -1-x points selon le nombre de cartes de ce joueur + de la banque.
BlackJackVSBlackJack => Lose VSBlackJack car la banque gagne TOUJOURS si elle a un BlackJack, ce n'est donc pas un Push !

Rester : Le joueur termine son tour. Aucun changement de points.
Tirer : Le joueur tire une carte. Si le total fait 22 ou plus, c'est un Bust. Si le total fait 21, le joueur termine immédiatement son tour. Aucun changement de points.
Doubler : Uniquement au début d'une manche. -2 points lors de la surenchère, le joueur ne tire qu'une carte. +4 points de bonus si Win.
Séparer : Uniquement au début d'une manche. Chaque carte forme le début d'une nouvelle main. Chaque main est traitée séparément (il peut y avoir des BlackJack !). Aucun changement de points.
Abandonner : Uniquement au début d'une manche SEULEMENT si l'assurance n'a pas été prise. -1 point mais immunisé contre tout autre retrait de points, y compris BlackJack. Termine la partie immédiatement si tous les joueurs abandonnent.
Assurance : Uniquement si la première carte du banquier est A. -1 point au début de la manche. Puis...
Si la banque avait effectivement BlackJack : +2 points de bonus. Sinon : le point est perdu.

Note : Selon la variante, A,10 peut être considéré comme un 21 mais pas un BlackJack contrairement à A,Figure (J,Q,K)
Règle spéciale : Le banquier ne reste pas s'il possède A,6 au début.
Mains particulières :
Si un joueur parvient a avoir deux BlackJack après avoir séparé, le +1 point de bonus n'est pas cumulé, mais vous l'obtenez MEME si la banque fait elle-même BlackJack.
Si un joueur possède 20 avec deux figures au début, il peut exécuter le pari d'avoir 21 en tirant un As. +5 points de bonus si gagné (au risque d'un Bust).
Si un joueur obtient 7,7,7 (donc il n'a pas séparé), +7 points de bonus.
Si un joueur gagne avec une main de 6 cartes ou plus, +2+2*(nbcartes-6) points de bonus. (6,7,8,9,10) -> (+2,+4,+6,+8,+10)


Un joueur peut participer tant que...
-Il a strictement plus de 0 points dans sa cagnotte.
-Il n'a pas fait (PLAYER_MAX_BUSTS_TODAY = 3) Bust ce jour.
-Un certain nombre de parties n'a pas encore été réalisé (MAX_DEALS_TODAY = 50).
-La journée n'est pas finie. Ses points se cumulent jusqu'à ce qu'il est (RESET_HOUR = 00:00 UTC). Le classement est alors réactualisé.

A chaque nouveau jour, un joueur peut recommencer avec 10 points initiaux.

"""
