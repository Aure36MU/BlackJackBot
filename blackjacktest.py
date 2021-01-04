import unittest
import blackjackbot
from blackjackbot import Player, Card, Hand, Deal


class TestPlayer(unittest.TestCase):
    pass


class TestCard(unittest.TestCase):
    def setUp(self):
        self.card_7_Heart = Card('7', 'Heart')
        self.card_hidden_Q_Spade = Card('Q', 'Spade', True)

    def testCardConstructorInvalid(self):
        self.assertRaises(TypeError, Card, 'B', 'Spade')
        self.assertRaises(TypeError, Card, '8', 'red')

    def testGetValue(self):
        self.assertEqual(self.card_7_Heart.getValue(), 7)
        self.assertEqual(self.card_hidden_Q_Spade.getValue(), 0)

    def testDisplay(self):
        blackjackbot.USE_EMOJI_TYPE = "Discord"
        self.assertEqual(self.card_7_Heart.display(),
                         Card.toEmoji(self.card_7_Heart, '7') + Card.toEmoji(self.card_7_Heart, 'Heart'))
        self.assertEqual(self.card_hidden_Q_Spade.display(),
                         Card.toEmoji(self.card_hidden_Q_Spade, '?') + Card.toEmoji(self.card_hidden_Q_Spade, '?'))
        blackjackbot.USE_EMOJI_TYPE = "Unicode"
        self.assertEqual(self.card_7_Heart.display(), "\u0037\u2665")
        self.assertEqual(self.card_hidden_Q_Spade.display(), "\u003F\u003F")

    def testStr(self):
        self.assertEqual(str(self.card_7_Heart), '7')
        self.assertEqual(str(self.card_hidden_Q_Spade), 'Q')


class TestHand(unittest.TestCase):
    def setUp(self):
        self.cards_standard = [Card('3', 'Club'), Card('8', 'Heart')]
        self.cards_bank = [Card('A', 'Diamond'), Card('K', 'Diamond', True)]
        self.hand_standard = Hand(1, self.cards_standard, 2.0, 0, False)
        self.hand_bank = Hand(0, self.cards_bank, 2.0, 0, False)

    def testAddCard(self):
        self.assertEqual(len(self.hand_standard.cards), 2)
        self.hand_standard.addCard(Card('2', 'Heart'))
        self.assertEqual(len(self.hand_standard.cards), 3)

    def testTakeLastCard(self):
        self.assertEqual(len(self.hand_standard.cards), 2)
        self.hand_standard.takeLastCard()
        self.assertEqual(len(self.hand_standard.cards), 1)

    def testReveal(self):
        pass

    def testHide(self):
        pass

    def testGetTotal(self):
        self.assertEqual(self.hand_standard.getTotal(), 11) #hand_standard has 3+8
        self.hand_standard.takeLastCard()
        self.assertEqual(self.hand_standard.getTotal(), 3) #hand_standard has 3
        self.assertEqual(self.hand_bank.getTotal(), 11) #hand_bank has A+K with K hidden
        self.hand_bank.revealAll()
        self.assertEqual(self.hand_bank.getTotal(), 21) #hand_bank has A+K
        self.hand_bank.addCard(Card('7', 'Club', True))
        self.assertEqual(self.hand_bank.getTotal(), 21) #hand_bank has A+K+7 with 7 hidden
        self.hand_bank.revealAll()
        self.assertEqual(self.hand_bank.getTotal(), 18) #hand_bank has A+K+7

    def testDisplay(self):
        pass



class TestDeal(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()