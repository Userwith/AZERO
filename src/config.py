import numpy as np
import json
import random
import copy
import time


class Main:
    minute_updater = []

    def __init__(self):
        self.world_tree = WorldTree()
        self.t = time.time()

    @staticmethod
    def minute_updater_register(updater):
        Main.minute_updater.append(updater)

    def start(self):
        while True:
            new_time = time.time()
          #  if new_time - self.t > 2:
            for i in Main.minute_updater:
                i()
            self.t = new_time


class Object:
    def __init__(self):
        self.wid = WorldTree.register(self)

    def delete(self):
        WorldTree.withdraw(self.wid)
        del self


class System(Object):
    def __init__(self):
        super().__init__()


class WorldTree(System):
    record = {}
    world_dict = {}

    def __init__(self):
        super().__init__()
        with open('../data/character.json', encoding='utf-8') as a:
            WorldTree.world_dict["character"] = json.load(a)
        with open('../data/organ.json', encoding='utf-8') as a:
            WorldTree.world_dict["organ"] = json.load(a)
        with open('../data/skill.json', encoding='utf-8') as a:
            WorldTree.world_dict["skill"] = json.load(a)
        with open('../data/magic.json', encoding='utf-8') as a:
            WorldTree.world_dict["magic"] = json.load(a)
        with open('../data/career.json', encoding='utf-8') as a:
            WorldTree.world_dict["career"] = json.load(a)
        with open('../data/feature.json', encoding='utf-8') as a:
            WorldTree.world_dict["feature"] = json.load(a)
        with open('../data/race.json', encoding='utf-8') as a:
            WorldTree.world_dict["race"] = json.load(a)
        with open('../data/status.json', encoding='utf-8') as a:
            WorldTree.world_dict["status"] = json.load(a)
        with open('../data/buff.json', encoding='utf-8') as a:
            WorldTree.world_dict["buff"] = json.load(a)
        with open('../data/block.json', encoding='utf-8') as a:
            WorldTree.world_dict["block"] = json.load(a)

    @classmethod
    def register(cls, obj):
        while True:
            wid = id(obj)
            if wid not in cls.record.keys():
                cls.record[wid] = obj
                break
        return wid

    @classmethod
    def withdraw(cls, wid):
        try:
            cls.record.pop(wid)
        except Exception:
            print("Error")

    @classmethod
    def get_status(cls, type, names: list):
        cache = []
        for i in names:
            for j in WorldTree.world_dict[type]:
                if i == j[0]:
                    cache.append(copy.deepcopy(j))
        return cache


class Event(Object):
    record = {}

    def __init__(self):
        super().__init__()

    @classmethod
    def register(cls, wid, obj):
        if wid not in cls.record.keys():
            cls.record[wid] = obj
        else:
            print("Error register")
        return wid

    @classmethod
    def withdraw(cls, wid):
        try:
            cls.record.pop(wid)
        except Exception:
            print("Error")


class Time(Object):

    def __init__(self):
        super().__init__()


class Coordinate(Object):
    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.map = np.array((self.x, self.y, self.z), dtype=Block)


class Substance(Object):
    def __init__(self, weight, volume, location):
        super().__init__()
        self.weight = weight
        self.volume = volume
        self.location = location


class Block(Substance):

    def __init__(self,name,location):
        self.slow_cache = {}
        self.fast_cache = {}
        self.slow_cache["name"] = name
        self.slow_cache['block'] = WorldTree.get_status("block",[name])[1]
        self.slow_cache['component'] = self.slow_cache['block']['成分占比']
        self.slow_cache['penetrability'] = self.slow_cache['block']['穿透性']
        self.slow_cache['transparency'] = self.slow_cache['block']['透明度']
        self.slow_cache['volume'] = 0.1*0.1*0.1
        self.slow_cache['weight'] = self.weight_calculator()

        super().__init__(weight=self.slow_cache['weight'], volume=self.slow_cache['volume'],location=location)

    def weight_calculator(self):
        weight = 0
        elements = WorldTree.get_status('element',self.slow_cache['block']['成分占比'].keys())
        for i in self.slow_cache['block']['成分占比'].keys():
            for j in elements:
                if j[0] == i:
                    weight += self.slow_cache['block']['成分占比'][i]*self.slow_cache["volume"]*j[1]['密度'][ self.slow_cache['block']['状态']]
        return weight


class Creature(Substance):
    def __init__(self, **kwargs):
        # property 顺序：[体，智，耐，魅，反，魔，幸]
        # status 顺序：[意识，SAN值，血氧浓度，饱食值，呼吸能力，消化能力，移动能力，反应能力，操作能力，视力，听力，嗅觉，免疫能力]
        # 器官属性顺序：[耐久度，重量，体积]
        self.slow_cache = {}
        self.fast_cache = {}
        ##角色清单初始化
        self.slow_cache['character'] = copy.deepcopy(WorldTree.get_status('character', ["character"])[0][1])
        self.slow_cache['name'] = self.slow_cache['character']['name']
        self.slow_cache['gender'] = self.slow_cache['character']['gender']
        self.slow_cache['feature'] = copy.deepcopy(WorldTree.get_status("feature", self.slow_cache['character']['feature']))
        self.slow_cache['race'] = copy.deepcopy(WorldTree.get_status("race", self.slow_cache['character']['race'])[0][1])
        self.slow_cache['magic'] = copy.deepcopy(WorldTree.get_status("magic", self.slow_cache['character']['magic']))
        self.slow_cache['career'] = copy.deepcopy(WorldTree.get_status("career", self.slow_cache['character']['career']))

        ##器官上限初始化
        self.slow_cache['organ'] = WorldTree.get_status("organ", self.slow_cache['race']['organ'])
        ##技能初始化
        self.slow_cache['skill'] = WorldTree.get_status("skill", self.slow_cache['character']['skill'])
        for i in self.slow_cache['feature']:
            if 'skill' in i[1].keys():
                self.slow_cache['skill'] += WorldTree.get_status("skill", i[1]['skill'])
        for i in self.slow_cache['organ']:
            if 'skill' in i[1].keys():
                self.slow_cache['skill'] += WorldTree.get_status("skill", i[1]['skill'])
        self.slow_cache['skill'] += WorldTree.get_status("skill", self.slow_cache['race']['skill'])
        for i in self.slow_cache['career']:
            if 'skill' in i[1].keys():
                self.slow_cache['skill'] += WorldTree.get_status("skill", i[1]['skill'])
        ##属性初始化
        self.slow_cache['property'] = np.array(self.slow_cache['race']['property'])
        for i in self.slow_cache['feature']:
            if 'property' in i[1].keys():
                self.slow_cache['property'] += i[1]['property']
        ##状态值上限初始化
        self.slow_cache['status'] = copy.deepcopy(WorldTree.get_status('status', ["status"])[0][1])
        # 魔法初始化
        self.slow_cache['magic'] = []
        ##状态值初始化
        self.fast_cache['status'] = copy.deepcopy(self.slow_cache['status'])
        self.fast_cache['age'] = copy.deepcopy(self.slow_cache['character']['age'])
        ##器官初始化
        self.fast_cache['organ'] = copy.deepcopy(self.slow_cache['organ'])
        ##buff初始化
        self.fast_cache['buff'] = []
        for i in self.slow_cache['feature']:
            if 'buff' in i[1].keys():
                self.fast_cache['buff'] += WorldTree.get_status("buff", i[1]['buff'])
        for i in self.slow_cache['organ']:
            if 'buff' in i[1].keys():
                self.fast_cache['buff'] += WorldTree.get_status("buff", i[1]['buff'])
        # 质量初始化
        self.fast_cache['weight'] = sum([i[1]['value'][1] for i in self.slow_cache['organ']]) * \
                                    self.slow_cache['race']['weight_bias']
        # 体积初始化
        self.fast_cache['volume'] = sum([i[1]['value'][2] for i in self.slow_cache['organ']])

        self.fast_cache['location'] = np.zeros(3,dtype=np.float64)
        super().__init__(self.fast_cache['weight'], self.fast_cache['volume'], self.fast_cache['location'] )

        Main.minute_updater_register(self.updater)

    def pain_caculator(self):
        max_organ = 0
        for i in self.slow_cache['organ']:
            if i[1]['value'][0] > max_organ:
                max_organ = i[1]['value'][0]

        max_differ_organ = 0
        for i in range(len(self.slow_cache['organ'])):
            differ_organ = self.slow_cache['organ'][i][1]['value'][0] - self.fast_cache['organ'][i][1]['value'][0]
            if differ_organ > max_differ_organ:
                max_differ_organ = differ_organ
        cache = (max_differ_organ / max_organ)
        if self.fast_cache['status']['疲劳'] > 0.9:
            cache += (self.fast_cache['status']['疲劳']-0.9)
        if self.fast_cache['status']['饱食度'] < 0.1:
            cache += (0.1-self.fast_cache['status']['饱食度'])
        if self.fast_cache['status']['血氧浓度'] < 0.1:
            cache += 10*(0.1-self.fast_cache['status']['血氧浓度'])
        if self.fast_cache['status']['意识'] < 0.5:
            return min(1, cache*np.log(1+self.fast_cache['status']['意识'])/np.log(2))
        else:
            return min(1,cache)

    def find_organ_upper(self, organ):
        for i in self.slow_cache['organ']:
            if organ in i[0]:
                return i[1]['value'][0]

    def organ_endurance_ratio(self, organ):
        organ_upper = 1e-5
        for i in self.slow_cache['organ']:
            if organ in i[0]:
                organ_upper = i[1]['value'][0]
        organ_curr = 0
        for i in self.fast_cache['organ']:
            if organ in i[0]:
                organ_curr = i[1]['value'][0]
        return (organ_curr / organ_upper)

    def consciousness_caculator(self):
        if self.fast_cache['status']['疲劳'] > 0.999999 or self.fast_cache['status']['饱食度'] < 1e-5 or self.fast_cache['status']['疼痛'] > 0.7 or self.fast_cache['status']['血氧浓度'] < 0.1 or self.fast_cache['status']['血液循环']< 0.1 or self.organ_endurance_ratio('大脑') < 0.5 or self.organ_endurance_ratio('血液') < 0.1:
            return max(0,self.fast_cache['status']['意识'] - 0.01 * (1-self.organ_endurance_ratio('大脑')) * (0.001*self.fast_cache['status']['疲劳']+0.001*(1-self.fast_cache['status']['饱食度']) + self.fast_cache['status']['疼痛'] + (1-self.organ_endurance_ratio(
                '血液')) + 0.3*(1-self.fast_cache['status']['血氧浓度']) + 0.3*(1-self.fast_cache['status']['血液循环'])))
        else:
            return min(1,self.fast_cache['status']['意识'] + 0.01*(1-self.fast_cache['status']['疲劳'])*self.fast_cache['status']['血液循环']*self.fast_cache['status']['血氧浓度']*self.fast_cache['status']['饱食度'])

    def SAN_caculator(self):
        return self.fast_cache['status']['意识'] * self.organ_endurance_ratio('大脑') * (
                1 - self.fast_cache['status']['疼痛'])

    def blood_oxygen_content_caculator(self):
        return max(0, min(1, self.fast_cache['status']['血氧浓度'] - (
                self.fast_cache['status']['血氧浓度'] / 5 * self.organ_endurance_ratio('血液')) *
                          self.fast_cache['status']['血液循环'] + self.fast_cache['status'][
                              '呼吸能力'] * self.organ_endurance_ratio('血液') * self.fast_cache['status']['意识'] *
                          self.fast_cache['status']['血液循环']))

    def blood_circulation_calculator(self):
        return self.organ_endurance_ratio('心脏')

    def digestive_calculator(self):
        return self.organ_endurance_ratio('胃') * self.fast_cache['status']['血液循环']

    def vision_calculator(self):
        return self.fast_cache['status']['意识']*(self.organ_endurance_ratio('左眼') + self.organ_endurance_ratio('右眼')) / 2

    def smell_calculator(self):
        return self.fast_cache['status']['意识']*self.organ_endurance_ratio('鼻子') * self.fast_cache['status']['呼吸能力']

    def hearing_calculator(self):
        return self.fast_cache['status']['意识']*(self.organ_endurance_ratio('左耳') + self.organ_endurance_ratio('右耳')) / 2

    def immunity_calculator(self):
        return (1 - self.fast_cache['status']['疲劳']) * self.organ_endurance_ratio('肝脏') * \
               self.fast_cache['status']['血液循环'] * (
                           self.organ_endurance_ratio('左肾') + self.organ_endurance_ratio('右肾')) / 2

    def breathe_calculator(self):
        return self.fast_cache['status']['血液循环'] * (
                    self.organ_endurance_ratio('左肺') + self.organ_endurance_ratio('右肺')) / 2

    def move_ability_calculator(self):
        return (1 - self.fast_cache['status']['疲劳']) * self.fast_cache['status']['血氧浓度'] * \
               self.fast_cache['status']['血液循环'] * self.fast_cache['status']['意识'] * (
                           1 - self.fast_cache['status']['疼痛']) * (
                           self.organ_endurance_ratio('左腿') + self.organ_endurance_ratio('右腿')) * (
                           self.organ_endurance_ratio('左脚') + self.organ_endurance_ratio('右脚')) / 4

    def operational_calculator(self):
        return (1 - self.fast_cache['status']['疲劳']) * self.fast_cache['status']['血氧浓度'] * \
               self.fast_cache['status']['血液循环'] * self.fast_cache['status']['意识'] * (
                           1 - self.fast_cache['status']['疼痛']) * (
                           self.organ_endurance_ratio('左臂') + self.organ_endurance_ratio('右臂')) * (
                           self.organ_endurance_ratio('左手') + self.organ_endurance_ratio('右手')) / 4


    def satiety_calculator(self):
        return max(0, self.fast_cache['status']['饱食度'] - self.fast_cache['status']['血液循环'] *
                   self.fast_cache['status']['呼吸能力'] / (60 * 24))

    def fatigue_calculator(self):
        return min(1, self.fast_cache['status']['疲劳'] + (1.5 - self.fast_cache['status']['血氧浓度']) / (10 * 60))



    def metabolic_updater(self):
        # 器官耐久度
        #
        # status 顺序：[疼痛值，意识，SAN值，血氧浓度，饱食值，血液循环能力，呼吸能力，消化能力，移动能力，反应能力，操作能力，视力，听力，嗅觉，免疫能力]

        """
        更新顺序：
        疼痛值公式： 默认0， max(器官耐久值上限-器官耐久值)/max(器官耐久值上限)
        意识公式：默认 1，（大脑耐久值/大脑耐久值上限）*（血液耐久值/血液耐久值上限）*（1-疼痛值）
        SAN值公式：大脑耐久值/大脑耐久值上限*意识
        血氧浓度：体重
        饱食值：默认 1
        血液循环能力：心脏耐久值
        :return:
        """
        self.fast_cache['status']['疼痛'] = self.pain_caculator()
        self.fast_cache['status']['意识'] = self.consciousness_caculator()
        self.fast_cache['status']['SAN'] = self.SAN_caculator()
        self.fast_cache['status']['疲劳'] = self.fatigue_calculator()
        self.fast_cache['status']['血液循环'] = self.blood_circulation_calculator()
        self.fast_cache['status']['呼吸能力'] = self.breathe_calculator()
        self.fast_cache['status']['消化能力'] = self.digestive_calculator()
        self.fast_cache['status']['视力'] = self.vision_calculator()
        self.fast_cache['status']['听力'] = self.hearing_calculator()
        self.fast_cache['status']['嗅觉'] = self.smell_calculator()
        self.fast_cache['status']['移动能力'] = self.move_ability_calculator()
        self.fast_cache['status']['操作能力'] = self.operational_calculator()
        self.fast_cache['status']['免疫能力'] = self.immunity_calculator()
        self.fast_cache['status']['血氧浓度'] = self.blood_oxygen_content_caculator()
        self.fast_cache['status']['饱食度'] = self.satiety_calculator()

    def self_healing_updater(self):
        for i in self.fast_cache['organ']:
            if i[1]['value'][0] > 0 and self.organ_endurance_ratio(i[0]) < 1:
                i[1]['value'][0] = min(self.find_organ_upper(i[0]),
                                       i[1]['value'][0] + 0.007 * self.fast_cache['status']['血液循环'] *
                                       self.fast_cache['status']['饱食度'] * (1 - self.fast_cache['status']['疲劳']))
            if self.fast_cache['status']['血氧浓度'] <= 1e-5:
                for j in ["心","肝","胃","脑","肺"]:
                    if j in i[0]:
                        i[1]['value'][0] = max(0, i[1]['value'][0] - 0.16)

            if self.fast_cache['status']['饱食度'] <= 1e-5:
                for j in ["心","肝","胃","脑","肺"]:
                    if j in i[0]:
                        i[1]['value'][0] = max(0, i[1]['value'][0] - 0.0006)

            if self.fast_cache['status']['血液循环'] <= 0:
                i[1]['value'][0] = max(0, i[1]['value'][0] - 0.07)

    def buff_updater(self):
        """
        buff类型分为一下几种：
        1. property:直接增加属性
        2. status: 改变状态
        3. organ: 改变器官
        4. special：特殊buff
        :return:
        """


    def updater(self):
        self.metabolic_updater()
        self.self_healing_updater()
        self.buff_updater()


if __name__ == "__main__":
    w = WorldTree()
    a = Creature()
    a.delete()
