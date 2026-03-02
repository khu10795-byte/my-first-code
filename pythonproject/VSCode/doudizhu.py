import random
import time

class Card:
    def __init__(self, suit, rank):
        self.suit = suit  # 花色：0-黑桃，1-红桃，2-梅花，3-方块，4-小王，5-大王
        self.rank = rank  # 点数：3-10，J=11，Q=12，K=13，A=14，2=15
    
    def __lt__(self, other):
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.suit < other.suit
    
    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    
    def __str__(self):
        suit_str = ['♠', '♥', '♣', '♦', '小王', '大王']
        rank_str = ['', '', '', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
        
        if self.suit >= 4:
            return suit_str[self.suit]
        return f"{suit_str[self.suit]}{rank_str[self.rank]}"

class Player:
    def __init__(self, player_id, is_ai=False):
        self.id = player_id
        self.hand = []
        self.is_landlord = False
        self.is_ai = is_ai
    
    def sort_hand(self):
        self.hand.sort()
    
    def show_hand(self):
        print(f"玩家{self.id}的手牌：")
        for i, card in enumerate(self.hand):
            print(f"[{i}]{card}", end=" ")
        print()

class DoudizhuGame:
    def __init__(self):
        self.players = [Player(0), Player(1, True), Player(2, True)]
        self.deck = []
        self.bottom = []
        self.current_player = 0
        self.landlord = -1
        self.last_cards = []
        self.last_player = -1
    
    def init_deck(self):
        self.deck = []
        # 生成普通牌
        for suit in range(4):
            for rank in range(3, 16):
                self.deck.append(Card(suit, rank))
        # 添加大小王
        self.deck.append(Card(4, 16))  # 小王
        self.deck.append(Card(5, 17))  # 大王
    
    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    def deal_cards(self):
        # 清空玩家手牌和底牌
        for player in self.players:
            player.hand = []
        self.bottom = []
        
        # 发牌给三个玩家
        for i in range(51):
            self.players[i % 3].hand.append(self.deck[i])
        # 剩余3张作为底牌
        for i in range(51, 54):
            self.bottom.append(self.deck[i])
        # 整理手牌
        for player in self.players:
            player.sort_hand()
    
    def bid_landlord(self):
        bids = [0, 0, 0]
        max_bid = 0
        max_bidder = -1
        
        print("开始叫地主...")
        
        # 轮流叫地主
        for i in range(3):
            player_index = (self.current_player + i) % 3
            player = self.players[player_index]
            
            if player.is_ai:
                # AI叫地主逻辑
                bid = 0
                # 简单AI：如果有王或多个2，就叫地主
                king_count = sum(1 for card in player.hand if card.rank in [16, 17])
                two_count = sum(1 for card in player.hand if card.rank == 15)
                if king_count >= 1 or two_count >= 2:
                    bid = 1
                bids[player_index] = bid
                print(f"玩家{player_index}叫分：{bid}")
            else:
                # 玩家叫地主
                bid = int(input(f"玩家{player_index}，请输入叫分（0-3）："))
                bids[player_index] = bid
            
            if bids[player_index] > max_bid:
                max_bid = bids[player_index]
                max_bidder = player_index
        
        # 确定地主
        if max_bidder != -1:
            self.landlord = max_bidder
            self.players[max_bidder].is_landlord = True
            # 地主获得底牌
            for card in self.bottom:
                self.players[max_bidder].hand.append(card)
            self.players[max_bidder].sort_hand()
            print(f"玩家{max_bidder}成为地主！")
            print("底牌：", end="")
            for card in self.bottom:
                print(card, end=" ")
            print()
        else:
            # 重新开始叫地主
            print("无人叫地主，重新开始...")
            self.bid_landlord()
    
    def check_card_type(self, cards):
        if not cards:
            return "空牌"
        if len(cards) == 1:
            return "单牌"
        if len(cards) == 2:
            if cards[0].rank == 16 and cards[1].rank == 17:
                return "王炸"
            elif cards[0].rank == cards[1].rank:
                return "对子"
            else:
                return "无效"
        if len(cards) == 3 and all(card.rank == cards[0].rank for card in cards):
            return "三张"
        if len(cards) == 4 and all(card.rank == cards[0].rank for card in cards):
            return "炸弹"
        # 顺子（5张及以上连续牌）
        if len(cards) >= 5:
            is_straight = True
            for i in range(1, len(cards)):
                if cards[i].rank != cards[i-1].rank + 1:
                    is_straight = False
                    break
            if is_straight:
                return "顺子"
        # 对子顺（3对及以上连续对子）
        if len(cards) >= 6 and len(cards) % 2 == 0:
            is_pair_straight = True
            for i in range(0, len(cards), 2):
                if i + 1 >= len(cards) or cards[i].rank != cards[i+1].rank:
                    is_pair_straight = False
                    break
                if i > 0 and cards[i].rank != cards[i-2].rank + 1:
                    is_pair_straight = False
                    break
            if is_pair_straight:
                return "对子顺"
        return "无效"
    
    def compare_cards(self, current, last):
        if not last:
            return True  # 空牌可以出任何牌
        
        current_type = self.check_card_type(current)
        last_type = self.check_card_type(last)
        
        if current_type == "无效" or last_type == "无效":
            return False
        
        # 炸弹比其他牌大
        if current_type == "炸弹" and last_type not in ["炸弹", "王炸"]:
            return True
        
        # 王炸最大
        if current_type == "王炸":
            return True
        
        # 牌型必须相同才能比较
        if current_type != last_type or len(current) != len(last):
            return False
        
        # 比较牌的大小
        return current[-1].rank > last[-1].rank
    
    def play_cards(self, player, cards):
        # 检查牌是否在玩家手中
        temp_hand = player.hand.copy()
        for card in cards:
            if card not in temp_hand:
                return False
            temp_hand.remove(card)
        
        # 检查牌型是否有效
        if self.check_card_type(cards) == "无效":
            return False
        
        # 检查是否能压过上家
        if not self.compare_cards(cards, self.last_cards):
            return False
        
        # 更新玩家手牌
        player.hand = temp_hand
        self.last_cards = cards
        self.last_player = player.id
        
        # 显示出牌
        print(f"玩家{player.id}出牌：", end="")
        for card in cards:
            print(card, end=" ")
        print()
        
        return True
    
    def ai_play(self):
        player = self.players[self.current_player]
        
        # 尝试出炸弹
        for i in range(len(player.hand) - 3):
            if player.hand[i].rank == player.hand[i+1].rank == player.hand[i+2].rank == player.hand[i+3].rank:
                bomb = player.hand[i:i+4]
                if self.compare_cards(bomb, self.last_cards):
                    return bomb
        
        # 尝试出对子
        for i in range(len(player.hand) - 1):
            if player.hand[i].rank == player.hand[i+1].rank:
                pair = player.hand[i:i+2]
                if self.compare_cards(pair, self.last_cards):
                    return pair
        
        # 尝试出单牌
        for card in player.hand:
            single = [card]
            if self.compare_cards(single, self.last_cards):
                return [card]
        
        # 无法出牌，返回空
        return []
    
    def start_game(self):
        # 初始化牌堆
        self.init_deck()
        # 洗牌
        self.shuffle_deck()
        # 发牌
        self.deal_cards()
        # 显示初始手牌
        for player in self.players:
            player.show_hand()
        # 叫地主
        self.bid_landlord()
        # 显示地主手牌
        self.players[self.landlord].show_hand()
        # 开始出牌
        self.current_player = self.landlord  # 地主先出牌
        self.last_cards = []
        self.last_player = -1
        
        while True:
            player = self.players[self.current_player]
            print(f"当前轮到玩家{self.current_player}出牌")
            
            cards = []
            if player.is_ai:
                # AI出牌
                time.sleep(1)  # 模拟思考时间
                cards = self.ai_play()
                if not cards:
                    print(f"玩家{self.current_player}选择过")
                else:
                    self.play_cards(player, cards)
            else:
                # 玩家出牌
                player.show_hand()
                input_str = input("请输入要出的牌的索引（空格分隔，输入-1表示过）：")
                if input_str == "-1":
                    print(f"玩家{self.current_player}选择过")
                else:
                    indices = list(map(int, input_str.split()))
                    cards = [player.hand[i] for i in indices if 0 <= i < len(player.hand)]
                    if not self.play_cards(player, cards):
                        print("出牌无效，请重新出牌！")
                        continue
            
            # 检查是否有人获胜
            if not player.hand:
                print(f"玩家{self.current_player}获胜！")
                break
            
            # 轮到下一个玩家
            self.current_player = (self.current_player + 1) % 3

if __name__ == "__main__":
    game = DoudizhuGame()
    game.start_game()