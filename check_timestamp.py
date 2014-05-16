#! /usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
import time
from selenium import webdriver

class CheckTimestamp(unittest.TestCase):

    def setUp(self):
        """Инициализация переменных для всех тестов"""
        self.driver = webdriver.Firefox()

    def tearDown(self):
        """Удаление переменных для всех тестов. Остановка приложения"""
        self.driver.close()
        if sys.exc_info()[0]:   
            print sys.exc_info()[0]

    def test_check_timestamp(self):

        result = True #результат проверок, если не изменится на False, то тест пройден

        ch_time = int(time.mktime(time.strptime(os.getenv('DATE'), '%Y-%m-%d %H:%M:%S')))#Перевод человекопонятного времени в unix timestamp
        self.driver.get('http://nsk.terminal.ru/')     
        head = self.driver.find_element_by_tag_name('head') #содержимое тега head
        scripts = head.find_elements_by_tag_name('script') #все скрипты
        links = head.find_elements_by_tag_name('link') #все подключаемые файлы

        for x in scripts:#выполняется поиск нужного скрипта, как толоко он найден - цикл прерывается
            if u'/compiled/js/main' in x.get_attribute('src'):
                script = x.get_attribute('src')[x.get_attribute('src').find('js?'):]
                break
	    
        for x in links:#выполняется поиск нужного файла стиля, как толоко он найден - цикл прерывается
            if u'/compiled/css/main' in x.get_attribute('href'):
                css = x.get_attribute('href')[x.get_attribute('href').find('css?'):]
                break
        
        if '?' in script and script:#отделяется версия от разширения, если нет знака-разделителся - тест завершается ошибкой
            script = script.split('?')
        else:
            print 'Не обнаружена версия js файла'
            print '-'*80
            assert False, (u'Wrong js name')

        if '?' in css and css:#отделяется версия от разширения, если нет знака-разделителся - тест завершается ошибкой
            css = css.split('?')
        else:
            print 'Не обнаружена версия css файла'
            print '-'*80
            assert False, (u'Wrong css name')

        files_dict = dict([script, css]) #результаты собираются в словарь

        if files_dict['js'] == files_dict['css']: #версии файлов сравниваются, если они разные - тест завершается ошибкой
            version = int(files_dict['js']) #версии равны, поэтому можно взять любое значение
            if version<ch_time: #если файлы сформированы раньше, чем да
                print 'Дата создания файлов меньше введенной'
                print 'Файлы от %s МСК' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(version)))
                print 'Введенная дата - %s МСК' %(os.getenv('DATE'))
                print '-'*80
                result = False
        else:
            print 'У CSS и JS файлов разная версия'
            print '-'*80
            assert False, (u'Different file versions')

        assert result, (u'Wrong versions')
        

