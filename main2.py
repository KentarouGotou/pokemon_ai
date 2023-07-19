import numpy as np
import matplotlib.pyplot as plt
from qlearning_agent import QLearningAgent
from buttle_world import ButtleWorld

# 行動：A，B，C，D
# 状態：HP16
# 報酬：勝ったら100，負けたら-100，引き分けは0, 相手よりもダメージが高いと+1, 相手よりもダメージが低いと-1

# 定数
NB_EPISODE = 100    # エピソード数
EPSILON = 0.1    # 探索率
ALPHA = 0.1      # 学習率
GAMMA = 0.90
ACTIONS = np.arange(4)  # 行動の集合
HP = 30

if __name__ == '__main__':
    buttle_env = ButtleWorld(hp = HP) # バトルフィールドの初期化
    init_state = buttle_env.init_state # 初期状態
    # エージェントの初期化
    agent = QLearningAgent(
        alpha=ALPHA,
        gamma=GAMMA,
        epsilon=EPSILON,  # 探索率
        actions=ACTIONS,   # 行動の集合
        observation=init_state)  # Q学習エージェント
    rewards = []    # 評価用報酬の保存
    is_end_episode = False  # バトルが終了してるかどうか？
    
    # 実験
    for episode in range(NB_EPISODE):
        print(episode)
        episode_reward = []  # 1エピソードの累積報酬
        while(is_end_episode == False): # バトルが終了するまで続ける
            agent_action, enemy_action = agent.act()  # 行動選択
            states, reward, is_end_episode = buttle_env.fight(agent_action, enemy_action)
            print("actions ", buttle_env.actions[agent_action],buttle_env.actions[enemy_action] , "state ", states, "result ", is_end_episode)
            agent.observe(states, reward)   # 状態と報酬の観測
            episode_reward.append(reward)
        rewards.append(np.sum(episode_reward))  # このエピソードの平均報酬を与える
        states = buttle_env.reset_state()  # 初期化
        agent.observe(states)    # エージェントを初期位置に
        is_end_episode = False
        
    # 結果のプロット
    plt.plot(np.arange(NB_EPISODE), rewards)
    plt.xlabel("episode")
    plt.ylabel("reward")
    plt.savefig("result.jpg")
    plt.show()