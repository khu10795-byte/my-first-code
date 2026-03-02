#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <string>
#include <ctime>
#include <sstream>

// 牌的结构体
typedef struct Card {
    int suit; // 花色：0-黑桃，1-红桃，2-梅花，3-方块，4-小王，5-大王
    int rank; // 点数：3-10，J=11，Q=12，K=13，A=14，2=15
    
    // 构造函数
    Card(int s, int r) : suit(s), rank(r) {}
    
    // 牌的大小比较
    bool operator<(const Card& other) const {
        if (rank != other.rank) {
            return rank < other.rank;
        }
        return suit < other.suit;
    }
    
    // 牌的相等比较
    bool operator==(const Card& other) const {
        return suit == other.suit && rank == other.rank;
    }
    
    // 牌的字符串表示
    std::string toString() const {
        std::string suit_str, rank_str;
        
        // 花色
        switch (suit) {
            case 0: suit_str = "♠"; break;
            case 1: suit_str = "♥"; break;
            case 2: suit_str = "♣"; break;
            case 3: suit_str = "♦"; break;
            case 4: return "小王";
            case 5: return "大王";
            default: suit_str = "";
        }
        
        // 点数
        switch (rank) {
            case 11: rank_str = "J"; break;
            case 12: rank_str = "Q"; break;
            case 13: rank_str = "K"; break;
            case 14: rank_str = "A"; break;
            case 15: rank_str = "2"; break;
            default: rank_str = std::to_string(rank);
        }
        
        return suit_str + rank_str;
    }
} Card;

// 玩家类
class Player {
public:
    std::vector<Card> hand; // 手牌
    int id; // 玩家ID
    bool isLandlord; // 是否是地主
    bool isAI; // 是否是AI
    
    Player(int playerId, bool ai = false) : id(playerId), isLandlord(false), isAI(ai) {}
    
    // 整理手牌
    void sortHand() {
        std::sort(hand.begin(), hand.end());
    }
    
    // 显示手牌
    void showHand() const {
        std::cout << "玩家" << id << "的手牌：";
        for (size_t i = 0; i < hand.size(); ++i) {
            std::cout << "[" << i << "]" << hand[i].toString();
            if (i < hand.size() - 1) std::cout << " ";
        }
        std::cout << std::endl;
    }
};

// 游戏类
class DoudizhuGame {
private:
    std::vector<Card> deck; // 牌堆
    std::vector<Card> bottom; // 底牌
    Player* players[3]; // 三个玩家
    int currentPlayer; // 当前玩家
    int landlord; // 地主玩家ID
    std::vector<Card> lastCards; // 上一次出的牌
    int lastPlayer; // 上一次出牌的玩家
    
public:
    DoudizhuGame() {
        // 初始化玩家
        players[0] = new Player(0); // 玩家1
        players[1] = new Player(1, true); // AI玩家2
        players[2] = new Player(2, true); // AI玩家3
        
        currentPlayer = 0;
        landlord = -1;
        lastPlayer = -1;
    }
    
    ~DoudizhuGame() {
        for (int i = 0; i < 3; ++i) {
            delete players[i];
        }
    }
    
    // 初始化牌堆
    void initDeck() {
        deck.clear();
        // 生成普通牌
        for (int suit = 0; suit < 4; ++suit) {
            for (int rank = 3; rank <= 15; ++rank) {
                deck.emplace_back(suit, rank);
            }
        }
        // 添加大小王
        deck.emplace_back(4, 16); // 小王
        deck.emplace_back(5, 17); // 大王
    }
    
    // 洗牌
    void shuffleDeck() {
        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(deck.begin(), deck.end(), g);
    }
    
    // 发牌
    void dealCards() {
        // 发牌给三个玩家
        for (int i = 0; i < 51; ++i) {
            players[i % 3]->hand.push_back(deck[i]);
        }
        // 剩余3张作为底牌
        for (int i = 51; i < 54; ++i) {
            bottom.push_back(deck[i]);
        }
        // 整理手牌
        for (int i = 0; i < 3; ++i) {
            players[i]->sortHand();
        }
    }
    
    // 叫地主
    void bidLandlord() {
        int bids[3] = {0, 0, 0};
        int maxBid = 0;
        int maxBidder = -1;
        
        std::cout << "开始叫地主..." << std::endl;
        
        // 轮流叫地主
        for (int i = 0; i < 3; ++i) {
            int playerIndex = (currentPlayer + i) % 3;
            if (players[playerIndex]->isAI) {
                // AI叫地主逻辑
                int bid = 0;
                // 简单AI：如果有王或多个2，就叫地主
                int kingCount = 0, twoCount = 0;
                for (const auto& card : players[playerIndex]->hand) {
                    if (card.rank == 16 || card.rank == 17) kingCount++;
                    if (card.rank == 15) twoCount++;
                }
                if (kingCount >= 1 || twoCount >= 2) {
                    bid = 1;
                }
                bids[playerIndex] = bid;
                std::cout << "玩家" << playerIndex << "叫分：" << bid << std::endl;
            } else {
                // 玩家叫地主
                int bid;
                std::cout << "玩家" << playerIndex << "，请输入叫分（0-3）：";
                std::cin >> bid;
                bids[playerIndex] = bid;
            }
            
            if (bids[playerIndex] > maxBid) {
                maxBid = bids[playerIndex];
                maxBidder = playerIndex;
            }
        }
        
        // 确定地主
        if (maxBidder != -1) {
            landlord = maxBidder;
            players[landlord]->isLandlord = true;
            // 地主获得底牌
            for (const auto& card : bottom) {
                players[landlord]->hand.push_back(card);
            }
            players[landlord]->sortHand();
            std::cout << "玩家" << landlord << "成为地主！" << std::endl;
            std::cout << "底牌：";
            for (const auto& card : bottom) {
                std::cout << card.toString() << " ";
            }
            std::cout << std::endl;
        } else {
            // 重新开始叫地主
            std::cout << "无人叫地主，重新开始..." << std::endl;
            bidLandlord();
        }
    }
    
    // 检查牌型
    std::string checkCardType(const std::vector<Card>& cards) {
        if (cards.empty()) return "空牌";
        if (cards.size() == 1) return "单牌";
        if (cards.size() == 2) {
            if (cards[0].rank == 16 && cards[1].rank == 17) {
                return "王炸";
            } else if (cards[0].rank == cards[1].rank) {
                return "对子";
            } else {
                return "无效";
            }
        }
        if (cards.size() == 3 && cards[0].rank == cards[1].rank && cards[1].rank == cards[2].rank) {
            return "三张";
        }
        if (cards.size() == 4 && cards[0].rank == cards[1].rank && cards[1].rank == cards[2].rank && cards[2].rank == cards[3].rank) {
            return "炸弹";
        }
        // 顺子（5张及以上连续牌）
        if (cards.size() >= 5) {
            bool isStraight = true;
            for (size_t i = 1; i < cards.size(); ++i) {
                if (cards[i].rank != cards[i-1].rank + 1) {
                    isStraight = false;
                    break;
                }
            }
            if (isStraight) {
                return "顺子";
            }
        }
        // 对子顺（3对及以上连续对子）
        if (cards.size() >= 6 && cards.size() % 2 == 0) {
            bool isPairStraight = true;
            for (size_t i = 0; i < cards.size(); i += 2) {
                if (i + 1 >= cards.size() || cards[i].rank != cards[i+1].rank) {
                    isPairStraight = false;
                    break;
                }
                if (i > 0 && cards[i].rank != cards[i-2].rank + 1) {
                    isPairStraight = false;
                    break;
                }
            }
            if (isPairStraight) {
                return "对子顺";
            }
        }
        return "无效";
    }
    
    // 比较牌的大小
    bool compareCards(const std::vector<Card>& current, const std::vector<Card>& last) {
        if (last.empty()) return true; // 空牌可以出任何牌
        
        std::string currentType = checkCardType(current);
        std::string lastType = checkCardType(last);
        
        if (currentType == "无效" || lastType == "无效") {
            return false;
        }
        
        // 炸弹比其他牌大
        if (currentType == "炸弹" && lastType != "炸弹" && lastType != "王炸") {
            return true;
        }
        
        // 王炸最大
        if (currentType == "王炸") {
            return true;
        }
        
        // 牌型必须相同才能比较
        if (currentType != lastType || current.size() != last.size()) {
            return false;
        }
        
        // 比较牌的大小
        return current.back().rank > last.back().rank;
    }
    
    // 玩家出牌
    bool playCards(Player* player, const std::vector<Card>& cards) {
        // 检查牌是否在玩家手中
        std::vector<Card> tempHand = player->hand;
        for (const auto& card : cards) {
            auto it = std::find(tempHand.begin(), tempHand.end(), card);
            if (it == tempHand.end()) {
                return false;
            }
            tempHand.erase(it);
        }
        
        // 检查牌型是否有效
        if (checkCardType(cards) == "无效") {
            return false;
        }
        
        // 检查是否能压过上家
        if (!compareCards(cards, lastCards)) {
            return false;
        }
        
        // 更新玩家手牌
        player->hand = tempHand;
        lastCards = cards;
        lastPlayer = player->id;
        
        // 显示出牌
        std::cout << "玩家" << player->id << "出牌：";
        for (const auto& card : cards) {
            std::cout << card.toString() << " ";
        }
        std::cout << std::endl;
        
        return true;
    }
    
    // AI出牌逻辑
    std::vector<Card> aiPlay() {
        Player* player = players[currentPlayer];
        // 简单AI：出最小的单牌
        if (lastCards.empty()) {
            // 首次出牌，出最小的牌
            if (!player->hand.empty()) {
                return {player->hand[0]};
            }
        } else {
            // 尝试压过上家
            for (size_t i = 0; i < player->hand.size(); ++i) {
                std::vector<Card> singleCard = {player->hand[i]};
                if (compareCards(singleCard, lastCards)) {
                    return singleCard;
                }
            }
        }
        // 无法出牌，返回空
        return {};
    }
    
    // 开始游戏
    void startGame() {
        // 初始化牌堆
        initDeck();
        // 洗牌
        shuffleDeck();
        // 发牌
        dealCards();
        // 显示初始手牌
        for (int i = 0; i < 3; ++i) {
            players[i]->showHand();
        }
        // 叫地主
        bidLandlord();
        // 显示地主手牌
        players[landlord]->showHand();
        // 开始出牌
        currentPlayer = landlord; // 地主先出牌
        lastCards.clear();
        lastPlayer = -1;
        
        while (true) {
            Player* player = players[currentPlayer];
            std::cout << "当前轮到玩家" << currentPlayer << "出牌" << std::endl;
            
            std::vector<Card> cards;
            if (player->isAI) {
                // AI出牌
                cards = aiPlay();
                if (cards.empty()) {
                    std::cout << "玩家" << currentPlayer << "选择过" << std::endl;
                } else {
                    playCards(player, cards);
                }
            } else {
                // 玩家出牌
                player->showHand();
                std::cout << "请输入要出的牌的索引（空格分隔，输入-1表示过）：";
                std::string input;
                std::getline(std::cin >> std::ws, input);
                if (input == "-1") {
                    std::cout << "玩家" << currentPlayer << "选择过" << std::endl;
                } else {
                    std::istringstream iss(input);
                    int index;
                    while (iss >> index) {
                        if (index >= 0 && index < player->hand.size()) {
                            cards.push_back(player->hand[index]);
                        }
                    }
                    if (!playCards(player, cards)) {
                        std::cout << "出牌无效，请重新出牌！" << std::endl;
                        continue;
                    }
                }
            }
            
            // 检查是否有人获胜
            if (player->hand.empty()) {
                std::cout << "玩家" << currentPlayer << "获胜！" << std::endl;
                break;
            }
            
            // 轮到下一个玩家
            currentPlayer = (currentPlayer + 1) % 3;
        }
    }
};

int main() {
    DoudizhuGame game;
    game.startGame();
    return 0;
}
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <string>
#include <ctime>
#include <sstream>

// 牌的结构体
typedef struct Card {
    int suit; // 花色：0-黑桃，1-红桃，2-梅花，3-方块，4-小王，5-大王
    int rank; // 点数：3-10，J=11，Q=12，K=13，A=14，2=15
    
    // 构造函数
    Card(int s, int r) : suit(s), rank(r) {}
    
    // 牌的大小比较
    bool operator<(const Card& other) const {
        if (rank != other.rank) {
            return rank < other.rank;
        }
        return suit < other.suit;
    }
    
    // 牌的相等比较
    bool operator==(const Card& other) const {
        return suit == other.suit && rank == other.rank;
    }
    
    // 牌的字符串表示
    std::string toString() const {
        std::string suit_str, rank_str;
        
        // 花色
        switch (suit) {
            case 0: suit_str = "♠"; break;
            case 1: suit_str = "♥"; break;
            case 2: suit_str = "♣"; break;
            case 3: suit_str = "♦"; break;
            case 4: return "小王";
            case 5: return "大王";
            default: suit_str = "";
        }
        
        // 点数
        switch (rank) {
            case 11: rank_str = "J"; break;
            case 12: rank_str = "Q"; break;
            case 13: rank_str = "K"; break;
            case 14: rank_str = "A"; break;
            case 15: rank_str = "2"; break;
            default: rank_str = std::to_string(rank);
        }
        
        return suit_str + rank_str;
    }
} Card;

// 玩家类
class Player {
public:
    std::vector<Card> hand; // 手牌
    int id; // 玩家ID
    bool isLandlord; // 是否是地主
    bool isAI; // 是否是AI
    
    Player(int playerId, bool ai = false) : id(playerId), isLandlord(false), isAI(ai) {}
    
    // 整理手牌
    void sortHand() {
        std::sort(hand.begin(), hand.end());
    }
    
    // 显示手牌
    void showHand() const {
        std::cout << "玩家" << id << "的手牌：";
        for (size_t i = 0; i < hand.size(); ++i) {
            std::cout << "[" << i << "]" << hand[i].toString();
            if (i < hand.size() - 1) std::cout << " ";
        }
        std::cout << std::endl;
    }
};

// 游戏类
class DoudizhuGame {
private:
    std::vector<Card> deck; // 牌堆
    std::vector<Card> bottom; // 底牌
    Player* players[3]; // 三个玩家
    int currentPlayer; // 当前玩家
    int landlord; // 地主玩家ID
    std::vector<Card> lastCards; // 上一次出的牌
    int lastPlayer; // 上一次出牌的玩家
    
public:
    DoudizhuGame() {
        // 初始化玩家
        players[0] = new Player(0); // 玩家1
        players[1] = new Player(1, true); // AI玩家2
        players[2] = new Player(2, true); // AI玩家3
        
        currentPlayer = 0;
        landlord = -1;
        lastPlayer = -1;
    }
    
    ~DoudizhuGame() {
        for (int i = 0; i < 3; ++i) {
            delete players[i];
        }
    }
    
    // 初始化牌堆
    void initDeck() {
        deck.clear();
        // 生成普通牌
        for (int suit = 0; suit < 4; ++suit) {
            for (int rank = 3; rank <= 15; ++rank) {
                deck.emplace_back(suit, rank);
            }
        }
        // 添加大小王
        deck.emplace_back(4, 16); // 小王
        deck.emplace_back(5, 17); // 大王
    }
    
    // 洗牌
    void shuffleDeck() {
        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(deck.begin(), deck.end(), g);
    }
    
    // 发牌
    void dealCards() {
        // 发牌给三个玩家
        for (int i = 0; i < 51; ++i) {
            players[i % 3]->hand.push_back(deck[i]);
        }
        // 剩余3张作为底牌
        for (int i = 51; i < 54; ++i) {
            bottom.push_back(deck[i]);
        }
        // 整理手牌
        for (int i = 0; i < 3; ++i) {
            players[i]->sortHand();
        }
    }
    
    // 叫地主
    void bidLandlord() {
        int bids[3] = {0, 0, 0};
        int maxBid = 0;
        int maxBidder = -1;
        
        std::cout << "开始叫地主..." << std::endl;
        
        // 轮流叫地主
        for (int i = 0; i < 3; ++i) {
            int playerIndex = (currentPlayer + i) % 3;
            if (players[playerIndex]->isAI) {
                // AI叫地主逻辑
                int bid = 0;
                // 简单AI：如果有王或多个2，就叫地主
                int kingCount = 0, twoCount = 0;
                for (const auto& card : players[playerIndex]->hand) {
                    if (card.rank == 16 || card.rank == 17) kingCount++;
                    if (card.rank == 15) twoCount++;
                }
                if (kingCount >= 1 || twoCount >= 2) {
                    bid = 1;
                }
                bids[playerIndex] = bid;
                std::cout << "玩家" << playerIndex << "叫分：" << bid << std::endl;
            } else {
                // 玩家叫地主
                int bid;
                std::cout << "玩家" << playerIndex << "，请输入叫分（0-3）：";
                std::cin >> bid;
                bids[playerIndex] = bid;
            }
            
            if (bids[playerIndex] > maxBid) {
                maxBid = bids[playerIndex];
                maxBidder = playerIndex;
            }
        }
        
        // 确定地主
        if (maxBidder != -1) {
            landlord = maxBidder;
            players[landlord]->isLandlord = true;
            // 地主获得底牌
            for (const auto& card : bottom) {
                players[landlord]->hand.push_back(card);
            }
            players[landlord]->sortHand();
            std::cout << "玩家" << landlord << "成为地主！" << std::endl;
            std::cout << "底牌：";
            for (const auto& card : bottom) {
                std::cout << card.toString() << " ";
            }
            std::cout << std::endl;
        } else {
            // 重新开始叫地主
            std::cout << "无人叫地主，重新开始..." << std::endl;
            bidLandlord();
        }
    }
    
    // 检查牌型
    std::string checkCardType(const std::vector<Card>& cards) {
        if (cards.empty()) return "空牌";
        if (cards.size() == 1) return "单牌";
        if (cards.size() == 2) {
            if (cards[0].rank == 16 && cards[1].rank == 17) {
                return "王炸";
            } else if (cards[0].rank == cards[1].rank) {
                return "对子";
            } else {
                return "无效";
            }
        }
        if (cards.size() == 3 && cards[0].rank == cards[1].rank && cards[1].rank == cards[2].rank) {
            return "三张";
        }
        if (cards.size() == 4 && cards[0].rank == cards[1].rank && cards[1].rank == cards[2].rank && cards[2].rank == cards[3].rank) {
            return "炸弹";
        }
        // 顺子（5张及以上连续牌）
        if (cards.size() >= 5) {
            bool isStraight = true;
            for (size_t i = 1; i < cards.size(); ++i) {
                if (cards[i].rank != cards[i-1].rank + 1) {
                    isStraight = false;
                    break;
                }
            }
            if (isStraight) {
                return "顺子";
            }
        }
        // 对子顺（3对及以上连续对子）
        if (cards.size() >= 6 && cards.size() % 2 == 0) {
            bool isPairStraight = true;
            for (size_t i = 0; i < cards.size(); i += 2) {
                if (i + 1 >= cards.size() || cards[i].rank != cards[i+1].rank) {
                    isPairStraight = false;
                    break;
                }
                if (i > 0 && cards[i].rank != cards[i-2].rank + 1) {
                    isPairStraight = false;
                    break;
                }
            }
            if (isPairStraight) {
                return "对子顺";
            }
        }
        return "无效";
    }
    
    // 比较牌的大小
    bool compareCards(const std::vector<Card>& current, const std::vector<Card>& last) {
        if (last.empty()) return true; // 空牌可以出任何牌
        
        std::string currentType = checkCardType(current);
        std::string lastType = checkCardType(last);
        
        if (currentType == "无效" || lastType == "无效") {
            return false;
        }
        
        // 炸弹比其他牌大
        if (currentType == "炸弹" && lastType != "炸弹" && lastType != "王炸") {
            return true;
        }
        
        // 王炸最大
        if (currentType == "王炸") {
            return true;
        }
        
        // 牌型必须相同才能比较
        if (currentType != lastType || current.size() != last.size()) {
            return false;
        }
        
        // 比较牌的大小
        return current.back().rank > last.back().rank;
    }
    
    // 玩家出牌
    bool playCards(Player* player, const std::vector<Card>& cards) {
        // 检查牌是否在玩家手中
        std::vector<Card> tempHand = player->hand;
        for (const auto& card : cards) {
            auto it = std::find(tempHand.begin(), tempHand.end(), card);
            if (it == tempHand.end()) {
                return false;
            }
            tempHand.erase(it);
        }
        
        // 检查牌型是否有效
        if (checkCardType(cards) == "无效") {
            return false;
        }
        
        // 检查是否能压过上家
        if (!compareCards(cards, lastCards)) {
            return false;
        }
        
        // 更新玩家手牌
        player->hand = tempHand;
        lastCards = cards;
        lastPlayer = player->id;
        
        // 显示出牌
        std::cout << "玩家" << player->id << "出牌：";
        for (const auto& card : cards) {
            std::cout << card.toString() << " ";
        }
        std::cout << std::endl;
        
        return true;
    }
    
    // AI出牌逻辑
    std::vector<Card> aiPlay() {
        Player* player = players[currentPlayer];
        // 简单AI：出最小的单牌
        if (lastCards.empty()) {
            // 首次出牌，出最小的牌
            if (!player->hand.empty()) {
                return {player->hand[0]};
            }
        } else {
            // 尝试压过上家
            for (size_t i = 0; i < player->hand.size(); ++i) {
                std::vector<Card> singleCard = {player->hand[i]};
                if (compareCards(singleCard, lastCards)) {
                    return singleCard;
                }
            }
        }
        // 无法出牌，返回空
        return {};
    }
    
    // 开始游戏
    void startGame() {
        // 初始化牌堆
        initDeck();
        // 洗牌
        shuffleDeck();
        // 发牌
        dealCards();
        // 显示初始手牌
        for (int i = 0; i < 3; ++i) {
            players[i]->showHand();
        }
        // 叫地主
        bidLandlord();
        // 显示地主手牌
        players[landlord]->showHand();
        // 开始出牌
        currentPlayer = landlord; // 地主先出牌
        lastCards.clear();
        lastPlayer = -1;
        
        while (true) {
            Player* player = players[currentPlayer];
            std::cout << "当前轮到玩家" << currentPlayer << "出牌" << std::endl;
            
            std::vector<Card> cards;
            if (player->isAI) {
                // AI出牌
                cards = aiPlay();
                if (cards.empty()) {
                    std::cout << "玩家" << currentPlayer << "选择过" << std::endl;
                } else {
                    playCards(player, cards);
                }
            } else {
                // 玩家出牌
                player->showHand();
                std::cout << "请输入要出的牌的索引（空格分隔，输入-1表示过）：";
                std::string input;
                std::getline(std::cin >> std::ws, input);
                if (input == "-1") {
                    std::cout << "玩家" << currentPlayer << "选择过" << std::endl;
                } else {
                    std::istringstream iss(input);
                    int index;
                    while (iss >> index) {
                        if (index >= 0 && index < player->hand.size()) {
                            cards.push_back(player->hand[index]);
                        }
                    }
                    if (!playCards(player, cards)) {
                        std::cout << "出牌无效，请重新出牌！" << std::endl;
                        continue;
                    }
                }
            }
            
            // 检查是否有人获胜
            if (player->hand.empty()) {
                std::cout << "玩家" << currentPlayer << "获胜！" << std::endl;
                break;
            }
            
            // 轮到下一个玩家
            currentPlayer = (currentPlayer + 1) % 3;
        }
    }
};

int main() {
    DoudizhuGame game;
    game.startGame();
    return 0;
}
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <string>
#include <ctime>
#include <sstream>

// 牌的结构体
typedef struct Card {
    int suit; // 花色：0-黑桃，1-红桃，2-梅花，3-方块，4-小王，5-大王
    int rank; // 点数：3-10，J=11，Q=12，K=13，A=14，2=15
    
    // 构造函数
    Card(int s, int r) : suit(s), rank(r) {}
    
    // 牌的大小比较
    bool operator<(const Card& other) const {
        if (rank != other.rank) {
            return rank < other.rank;
        }
        return suit < other.suit;
    }
    
    // 牌的相等比较
    bool operator==(const Card& other) const {
        return suit == other.suit && rank == other.rank;
    }
    
    // 牌的字符串表示
    std::string toString() const {
        std::string suit_str, rank_str;
        
        // 花色
        switch (suit) {
            case 0: suit_str = "♠"; break;
            case 1: suit_str = "♥"; break;
            case 2: suit_str = "♣"; break;
            case 3: suit_str = "♦"; break;
            case 4: return "小王";
            case 5: return "大王";
            default: suit_str = "";
        }
        
        // 点数
        switch (rank) {
            case 11: rank_str = "J"; break;
            case 12: rank_str = "Q"; break;
            case 13: rank_str = "K"; break;
            case 14: rank_str = "A"; break;
            case 15: rank_str = "2"; break;
            default: rank_str = std::to_string(rank);
        }
        
        return suit_str + rank_str;
    }
} Card;

// 玩家类
class Player {
public:
    std::vector<Card> hand; // 手牌
    int id; // 玩家ID
    bool isLandlord; // 是否是地主
    bool isAI; // 是否是AI
    
    Player(int playerId, bool ai = false) : id(playerId), isLandlord(false), isAI(ai) {}
    
    // 整理手牌
    void sortHand() {
        std::sort(hand.begin(), hand.end());
    }
    
    // 显示手牌
    void showHand() const {
        std::cout << "玩家" << id << "的手牌：";
        for (size_t i = 0; i < hand.size(); ++i) {
            std::cout << "[" << i << "]" << hand[i].toString();
            if (i < hand.size() - 1) std::cout << " ";
        }
        std::cout << std::endl;
    }
};

// 游戏类
class DoudizhuGame {
private:
    std::vector<Card> deck; // 牌堆
    std::vector<Card> bottom; // 底牌
    Player* players[3]; // 三个玩家
    int currentPlayer; // 当前玩家
    int landlord; // 地主玩家ID
    std::vector<Card> lastCards; // 上一次出的牌
    int lastPlayer; // 上一次出牌的玩家
    
public:
    DoudizhuGame() {
        // 初始化玩家
        players[0] = new Player(0); // 玩家1
        players[1] = new Player(1, true); // AI玩家2
        players[2] = new Player(2, true); // AI玩家3
        
        currentPlayer = 0;
        landlord = -1;
        lastPlayer = -1;
    }
    
    ~DoudizhuGame() {
        for (int i = 0; i < 3; ++i) {
            delete players[i];
        }
    }
    
    // 初始化牌堆
    void initDeck() {
        deck.clear();
        // 生成普通牌
        for (int suit = 0; suit < 4; ++suit) {
            for (int rank = 3; rank <= 15; ++rank) {
                deck.emplace_back(suit, rank);
            }
        }
        // 添加大小王
        deck.emplace_back(4, 16); // 小王
        deck.emplace_back(5, 17); // 大王
    }
    
    // 洗牌
    void shuffleDeck() {
        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(deck.begin(), deck.end(), g);
    }
    
    // 发牌
    void dealCards() {
        // 发牌给三个玩家
        for (int i = 0; i < 51; ++i) {
            players[i % 3]->hand.push_back(deck[i]);
        }
        // 剩余3张作为底牌
        for (int i = 51; i < 54; ++i) {
            bottom.push_back(deck[i]);
        }
        // 整理手牌
        for (int i = 0; i < 3; ++i) {
            players[i]->sortHand();
        }
    }
    
    // 叫地主
    void bidLandlord() {
        int bids[3] = {0, 0, 0};
        int maxBid = 0;
        int maxBidder = -1;
        
        std::cout << "开始叫地主..." << std::endl;
        
        // 轮流叫地主
        for (int i = 0; i < 3; ++i) {
            int playerIndex = (currentPlayer + i) % 3;
            if (players[playerIndex]->isAI) {
                // AI叫地主逻辑
                int bid = 0;
                // 简单AI：如果有王或多个2，就叫地主
                int kingCount = 0, twoCount = 0;
                for (const auto& card : players[playerIndex]->hand) {
                    if (card.rank == 16 || card.rank == 17) kingCount++;
                    if (card.rank == 15) twoCount++;
                }
                if (kingCount >= 1 || twoCount >= 2) {
                    bid = 1;
                }
                bids[playerIndex] = bid;
                std::cout << "玩家" << playerIndex << "叫分：" << bid << std::endl;
            } else {
                // 玩家叫地主
                int bid;
                std::cout << "玩家" << playerIndex << "，请输入叫分（0-3）：";
                std::cin >> bid;
                bids[playerIndex] = bid;
            }
            
            if (bids[playerIndex] > maxBid) {
                maxBid = bids[playerIndex];
                maxBidder = playerIndex;
            }
        }
        
        // 确定地主
        if (maxBidder != -1) {
            landlord = maxBidder;
            players[landlord]->isLandlord = true;
            // 地主获得底牌
            for (const auto& card : bottom) {
                players[landlord]->hand.push_back(card);
            }
            players[landlord]->sortHand();
            std::cout << "玩家" << landlord << "成为地主！" << std::endl;
            std::cout << "底牌：";
            for (const auto& card : bottom) {
                std::cout << card.toString() << " ";
            }
            std::cout << std::endl;
        } else {
            // 重新开始叫地主
            std::cout << "无人叫地主，重新开始..." << std::endl;
            bidLandlord();
        }
    }
    
    // 检查牌型
    std::string checkCardType(const std::vector<Card>& cards) {
        if (cards.empty()) return "空牌";
        if (cards.size() == 1) return "单牌";
        if (cards.size() == 2) {
            if (cards[0].rank == 16 && cards[1].rank == 17) {
                return "王炸";
            } else if (cards[0].rank == cards[1].rank) {
                return "对子";
            } else {
                return "无效";
            }
        }
        if (cards.size() == 3 && cards[0].rank == cards[1].rank && cards[1].rank == cards[2].rank) {
            return "三张";
        }
        if (cards.size() == 4 && cards[0].rank == cards[1].rank && cards[1].rank == cards[2].rank && cards[2].rank == cards[3].rank) {
            return "炸弹";
        }
        // 顺子（5张及以上连续牌）
        if (cards.size() >= 5) {
            bool isStraight = true;
            for (size_t i = 1; i < cards.size(); ++i) {
                if (cards[i].rank != cards[i-1].rank + 1) {
                    isStraight = false;
                    break;
                }
            }
            if (isStraight) {
                return "顺子";
            }
        }
        // 对子顺（3对及以上连续对子）
        if (cards.size() >= 6 && cards.size() % 2 == 0) {
            bool isPairStraight = true;
            for (size_t i = 0; i < cards.size(); i += 2) {
                if (i + 1 >= cards.size() || cards[i].rank != cards[i+1].rank) {
                    isPairStraight = false;
                    break;
                }
                if (i > 0 && cards[i].rank != cards[i-2].rank + 1) {
                    isPairStraight = false;
                    break;
                }
            }
            if (isPairStraight) {
                return "对子顺";
            }
        }
        return "无效";
    }
    
    // 比较牌的大小
    bool compareCards(const std::vector<Card>& current, const std::vector<Card>& last) {
        if (last.empty()) return true; // 空牌可以出任何牌
        
        std::string currentType = checkCardType(current);
        std::string lastType = checkCardType(last);
        
        if (currentType == "无效" || lastType == "无效") {
            return false;
        }
        
        // 炸弹比其他牌大
        if (currentType == "炸弹" && lastType != "炸弹" && lastType != "王炸") {
            return true;
        }
        
        // 王炸最大
        if (currentType == "王炸") {
            return true;
        }
        
        // 牌型必须相同才能比较
        if (currentType != lastType || current.size() != last.size()) {
            return false;
        }
        
        // 比较牌的大小
        return current.back().rank > last.back().rank;
    }
    
    // 玩家出牌
    bool playCards(Player* player, const std::vector<Card>& cards) {
        // 检查牌是否在玩家手中
        std::vector<Card> tempHand = player->hand;
        for (const auto& card : cards) {
            auto it = std::find(tempHand.begin(), tempHand.end(), card);
            if (it == tempHand.end()) {
                return false;
            }
            tempHand.erase(it);
        }
        
        // 检查牌型是否有效
        if (checkCardType(cards) == "无效") {
            return false;
        }
        
        // 检查是否能压过上家
        if (!compareCards(cards, lastCards)) {
            return false;
        }
        
        // 更新玩家手牌
        player->hand = tempHand;
        lastCards = cards;
        lastPlayer = player->id;
        
        // 显示出牌
        std::cout << "玩家" << player->id << "出牌：";
        for (const auto& card : cards) {
            std::cout << card.toString() << " ";
        }
        std::cout << std::endl;
        
        return true;
    }
    
    // AI出牌逻辑
    std::vector<Card> aiPlay() {
        Player* player = players[currentPlayer];
        // 简单AI：出最小的单牌
        if (lastCards.empty()) {
            // 首次出牌，出最小的牌
            if (!player->hand.empty()) {
                return {player->hand[0]};
            }
        } else {
            // 尝试压过上家
            for (size_t i = 0; i < player->hand.size(); ++i) {
                std::vector<Card> singleCard = {player->hand[i]};
                if (compareCards(singleCard, lastCards)) {
                    return singleCard;
                }
            }
        }
        // 无法出牌，返回空
        return {};
    }
    
    // 开始游戏
    void startGame() {
        // 初始化牌堆
        initDeck();
        // 洗牌
        shuffleDeck();
        // 发牌
        dealCards();
        // 显示初始手牌
        for (int i = 0; i < 3; ++i) {
            players[i]->showHand();
        }
        // 叫地主
        bidLandlord();
        // 显示地主手牌
        players[landlord]->showHand();
        // 开始出牌
        currentPlayer = landlord; // 地主先出牌
        lastCards.clear();
        lastPlayer = -1;
        
        while (true) {
            Player* player = players[currentPlayer];
            std::cout << "当前轮到玩家" << currentPlayer << "出牌" << std::endl;
            
            std::vector<Card> cards;
            if (player->isAI) {
                // AI出牌
                cards = aiPlay();
                if (cards.empty()) {
                    std::cout << "玩家" << currentPlayer << "选择过" << std::endl;
                } else {
                    playCards(player, cards);
                }
            } else {
                // 玩家出牌
                player->showHand();
                std::cout << "请输入要出的牌的索引（空格分隔，输入-1表示过）：";
                std::string input;
                std::getline(std::cin >> std::ws, input);
                if (input == "-1") {
                    std::cout << "玩家" << currentPlayer << "选择过" << std::endl;
                } else {
                    std::istringstream iss(input);
                    int index;
                    while (iss >> index) {
                        if (index >= 0 && index < player->hand.size()) {
                            cards.push_back(player->hand[index]);
                        }
                    }
                    if (!playCards(player, cards)) {
                        std::cout << "出牌无效，请重新出牌！" << std::endl;
                        continue;
                    }
                }
            }
            
            // 检查是否有人获胜
            if (player->hand.empty()) {
                std::cout << "玩家" << currentPlayer << "获胜！" << std::endl;
                break;
            }
            
            // 轮到下一个玩家
            currentPlayer = (currentPlayer + 1) % 3;
        }
    }
};

int main() {
    DoudizhuGame game;
    game.startGame();
    return 0;
}