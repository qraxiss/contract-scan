from collections import defaultdict
from json import load
import re


class Generator:
    social_medias = ['telegram', 'site', 'twitter',
                     'gitbook', 'medium', 'github', 'linktree']

    @staticmethod
    def add_others(func):
        def inner(*args, **kwargs):
            keys = func(*args, **kwargs)
            for social in Generator.social_medias:
                if social not in keys:
                    keys[social] = keys['other']
            del keys['other']
            return keys
        return inner

    def __init__(self, info: dict) -> None:
        self.info = info
        self.research = ['inu', 'token', 'project', 'dao', 'coin', 'official']

        self.formatter()

    @property
    @add_others
    def words(self):
        return load(open('script/generator/words.json', 'r'))

    def formatter(self) -> str:
        for key, value in self.info.items():
            value = value.lower()
            value = re.sub(r"[\u3041-\u3096]", "", value)
            value = re.sub(r"[\u4e00-\u9fff]", "", value)
            for i in ".:;,-?/&$*+‘|'":
                value = value.replace(i, '_')
            self.info[key] = value.split(' ')

    @property
    def words_combo(self) -> dict:
        return {
            "thesymbol_word": lambda site: self.words_combinator(site, '', 'next', '_', True),
            "words_symbol": lambda site: self.words_combinator(site, '', 'back', '_', True),
            "wordssymbol": lambda site: self.words_combinator(site, '', 'back', '', True),
            "symbol_words": lambda site: self.words_combinator(site, '_', 'next', '_', True),
            "symbolwords": lambda site: self.words_combinator(site, '', 'next', '', True),
            "name1name2words": lambda site: self.words_combinator(site, '', 'next', ''),
            "name1_name2_words": lambda site: self.words_combinator(site, '_', 'next', '_'),
            "name1name2_words": lambda site: self.words_combinator(site, '', 'next', '_'),
            "wordsname1name2": lambda site: self.words_combinator(site, '', 'back', ''),
            "words_name1_name2": lambda site: self.words_combinator(site, '_', 'back', '_'),
            "words_name1name2": lambda site: self.words_combinator(site, '', 'back', '_'),
            "name1name2_words_": lambda site: self.words_combinator(site, '', 'next', '_', False, True),
            "name1-name2-words": lambda site: self.words_combinator(site, '-', 'next', '-'),
            "name1name2-words": lambda site: self.words_combinator(site, '', 'next', '-'),
            "symbol-words": lambda site: self.words_combinator(site, '-', 'next', '-', True),
        }

    @property
    @add_others
    def operation_combo(self) -> dict:
        methods = list(self.words_combo.values())
        return {
            'telegram': methods[:-4],
            'site': [
                self.words_combo[method]
                for method in ['name1name2words',
                               'name1_name2_words',
                               'name1name2_words',
                               'symbol-words',
                               'symbolwords']
            ],
            'twitter': [
                self.words_combo[method]
                for method in ['name1name2words',
                               'name1name2_words',
                               'name1_name2_words',
                               'symbol_words',
                               'symbolwords',
                               'name1name2_words_',
                               'words_name1name2',
                               'wordsname1name2']
            ],
            'other': [
                self.words_combo[method]
                for method in ['wordsname1name2',
                               'name1-name2-words',
                               'name1name2-words',
                               'symbol-words',
                               'symbolwords',
                               'name1name2words']
            ],
        }

    def concater(self):
        pass

    def words_combinator(self, site: str, sep_concat: str, where: str, 
                         sep_words: str, symbol: bool = False, 
                         endswith_underscore: bool = False, 
                         concat_name = None) -> list:
        words = self.words[site]

        result = self.combinator(site, sep_concat)

        match site, where:
            case 'telegram', 'back':
                words = self.words['words_telegram']
        
        if not concat_name:
            concat_name = sep_concat.join(self.info['name'])
            name = self.info['name']
        else:
            name = concat_name
            concat_name = sep_concat.join(concat_name)

        concat_symbol = sep_concat.join(self.info['symbol'])

        the = 'the' + sep_concat
        starts_with_the = self.info['name'][0] == 'the'


        match where, starts_with_the, symbol, endswith_underscore:
            case 'next', True, False, False:  # the varsa ve sembol değil ise
                def concater_without_the(word): return concat_name + sep_words + word
                result += list(map(concater_without_the, words))

            case 'next', True, True, False:  # the varsa ve sembol ise
                def concater_without_the(word): return concat_symbol + sep_words + word
                result += list(map(concater_without_the, words))

            case 'next', False, False, False:  # the yoksa ve sembol değil ise
                def concater_without_the(word): return concat_name + sep_words + word
                def concater_with_the(word): return the + concat_name + sep_words + word
                result += list(map(concater_without_the, words)) + list(map(concater_with_the, words))

            case 'next', False, True, False:  # the yoksa ve sembol ise
                def concater_without_the(word): return concat_symbol + sep_words + word
                def concater_with_the(word): return the + concat_symbol + sep_words + word
                result += list(map(concater_without_the, words)) + list(map(concater_with_the, words))

            case 'next', False, False, True:  # the yoksa ve _ ile bitiyorsa
                def concater_without_the(word): return concat_symbol + sep_words + word + '_'
                def concater_with_the(word): return the + concat_symbol + sep_words + word + '_'
                result += list(map(concater_without_the, words)) + list(map(concater_with_the, words))

            case 'next', True, False, True:  # the varsa ve _ ile bitiyorsa
                def concater_without_the(word): return concat_symbol + sep_words + word + '_'
                result += list(map(concater_without_the, words))

            case 'back', False, False, False:  # the yoksa ve sembol değil ise
                def concater_without_the(word): return word + sep_words + concat_name
                result += list(map(concater_without_the, words))

            case 'back', False, True, False:  # the yoksa ve sembol ise ise
                def concater_without_the(word): return word + sep_words + concat_symbol
                result += list(map(concater_without_the, words))

        # if 'site' == site:
        #     if name[-1] in self.research:   
        #         result += self.words_combinator(site, sep_concat, where, sep_words, 
        #                                         symbol, endswith_underscore, self.info['name'][:-1])

        return result



    def combinator(self, site: str, sep_concat: str, concat_name = None) -> list:
        def joiner(text, sep): return sep.join(text)

        if not concat_name:
            concat_name = sep_concat.join(self.info['name'])
            name = self.info['name']
        else:
            name = concat_name
            concat_name = sep_concat.join(concat_name)


        if name[0] == 'the':
            the = ''
        else:
            the = 'the'

        match len(self.info['symbol']):
            case 1:
                symbol = joiner(self.info['symbol'], '')
            case _:
                symbol = joiner(self.info['symbol'], sep_concat)

        special = list()

        match site:
            case 'twitter':
                special = list({
                    'name': joiner(name, '') + '_',
                    'symbol': symbol + '_',
                    'name_sep': joiner(name, sep_concat) + '_',
                }.values())

        result = list({
            'name': joiner(name, ''),
            'name_sep': joiner(name, sep_concat),
            'symbol': symbol,
            'thename': the + joiner(name, ''),
            'thename_sep': f'{the}{sep_concat}' + joiner(name, sep_concat),
            'thesymbol': the + joiner(self.info['symbol'], ''),
            'thesymbol_sep': f'{the}{sep_concat}' + joiner(self.info['symbol'], sep_concat),
            'namesymbol' : joiner(name, '') + symbol,
            'symbolname' : symbol + joiner(name, ''),
        }.values())

        # if 'site' == site:
        #     if name[-1] in self.research:   
        #         result += self.combinator(site, sep_concat, self.info['name'][:-1])
        
        return list(filter(lambda x : False if x[0] == '_' else True, result + special))
        




    @property
    def combinations(self):
        result = defaultdict(set)
        for operaiton, methods in self.operation_combo.items():
            for method in methods:
                result[operaiton].update(method(operaiton))
        return result
