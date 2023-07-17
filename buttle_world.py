import copy

class ButtleWorld:
    def __init__(self, hp=16):
        # バトルフィールドの初期化
        self.agent_init_state = hp
        self.enemy_init_state = hp
        self.init_state = (self.agent_init_state, self.enemy_init_state)
        # それぞれのHPの状態
        self.state = copy.deepcopy(self.init_state)
        
        self.actions = ["A", "B", "C", "D"]
        self.damage = {
            "A": 1,
            "B": 5,
            "C": 10,
            "D": 0
        }
        
    def fight(self, agent_action, enemy_action):
        """
            行動の実行
            状態, 報酬、終了したかを返却
        """
        agent_hp, enemy_hp = copy.deepcopy(self.state)
        
        # ダメージ計算
        enemy_damage = self.damage[self.actions[enemy_action]]
        agent_damage = self.damage[self.actions[agent_action]]
        
        # HPの更新
        self.agent_state = agent_hp - enemy_damage
        self.enemy_state = enemy_hp - agent_damage
        self.state = (self.agent_state, self.enemy_state)
        
        if self.agent_state <= 0 and self.enemy_state > 0:# エージェントの敗北
            reward = -100
            is_end_episode = True
            print("lose")
        elif self.enemy_state <= 0 and self.agent_state > 0:# エージェントの勝利
            reward = 100
            is_end_episode = True
            print("win")
        elif self.agent_state <= 0 and self.enemy_state <= 0:# 引き分け
            reward = 0
            is_end_episode = True
            print("draw")
        else:
            if agent_damage > enemy_damage:
                reward = 1
            elif agent_damage < enemy_damage:
                reward = -1
            else:
                reward = 0
            is_end_episode = False
        return self.state, reward, is_end_episode
        
    def reset_state(self):
        self.state = self.init_state
        return self.init_state