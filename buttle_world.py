import copy

class ButtleWorld:
    def __init__(self, hp=16):
        # バトルフィールドの初期化
        # HPの初期化
        self.agent_init_state = hp
        self.enemy_init_state = hp / 2
        # バフの初期化
        self.agent_init_buff = False
        self.enemy_init_buff = False
        self.init_state = (
            self.agent_init_state, 
            self.enemy_init_state, 
            self.agent_init_buff, 
            self.enemy_init_buff
            )
        # それぞれのHPの状態
        self.state = copy.deepcopy(self.init_state)
        # 行動の初期化
        self.actions = ["A", "B", "C", "D"]
        self.damage = {
            "A": 1,
            "B": 5,
            "C": 10,
            "D": 0 #バフ
        }
        
    def fight(self, agent_action, enemy_action):
        """
            行動の実行
            状態, 報酬、終了したかを返却
        """
        agent_hp, enemy_hp , agent_buff, enemy_buff = copy.deepcopy(self.state)
        
        # ダメージ計算
        enemy_damage = self.damage[self.actions[enemy_action]]
        agent_damage = self.damage[self.actions[agent_action]]
        if agent_buff:
            agent_damage = agent_damage * 20
        if enemy_buff:
            enemy_damage = enemy_damage * 20
        
        # HPの更新
        agent_hp = agent_hp - enemy_damage
        enemy_hp = enemy_hp - agent_damage
        # バフの更新
        if self.actions[agent_action] == "D":
            agent_buff = True
        if self.actions[enemy_action] == "D":
            enemy_buff = True
        # 状態の更新
        self.state = (agent_hp, enemy_hp, agent_buff, enemy_buff)
        
        if agent_hp <= 0 and enemy_hp > 0:# エージェントの敗北
            reward = -100
            is_end_episode = True
            print("lose")
        elif enemy_hp <= 0 and agent_hp > 0:# エージェントの勝利
            reward = 100
            is_end_episode = True
            print("win")
        elif agent_hp <= 0 and enemy_hp <= 0:# 引き分け
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