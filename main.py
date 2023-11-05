import re
from sys import exit
from collections import deque
from collections import UserDict
from datetime import datetime


class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):

    def __init__(self, value):

        self.value = value
        self.today = datetime.today().date()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):

        sovp = re.findall('^(\d){4}-(\d){2}-(\d){2}$', new_value)
        if sovp != []:
            self.__value = datetime.strptime(new_value, '%Y-%m-%d')
        else:
            raise ValueError

    def __str__(self):
        return self.value


class Name(Field):
    ...


class Phone(Field):

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):

        # '^(?:[( )-]*\d){10}[()-]*$' # UA-10
        sovp = re.findall('^(\d){10}$', new_value)
        if sovp != []:
            while not sovp[0].isdigit():
                check_dig = sovp[0]
                for char in check_dig:
                    if not char.isdigit():
                        sovp[0] = sovp[0].replace(char, '')
            self.__value = new_value
        else:
            raise ValueError

    def __str__(self):
        return self.value


class Iterable:
    MAX_VALUE = 5

    def __init__(self):
        self.current_value = 0

    def __next__(self):

        if self.current_value < self.MAX_VALUE:
            self.current_value += 1
            return self.current_value
        raise StopIteration


class Cust_iter:

    def __iter__(self):
        return Iterable()


class Record:
    
    def __init__(self, name):

        self.name = Name(name)
        self.phones = []
        self.birthday = ''

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = (Birthday(birthday))

    def days_to_birthday(self):

        if self.birthday:
            today_date = datetime(
                year=self.birthday.value.year, month=today.month, day=today.day)
            if today_date.date() < self.birthday.value.date():
                result = str((self.birthday.value.date() -
                        today_date.date()).days) + ' days...'
            elif today_date.date() > self.birthday.value.date():
                today_date = datetime(
                    year=self.birthday.value.year-1, month=today.month, day=today.day)
                result = str((self.birthday.value.date() -
                        today_date.date()).days) + ' days...'
            else:
                result = 'TODAY is Birthday!'
            return result
        else:
            return ''

    def edit_phone(self, old, new):

        edit_phone_result = False
        for ph in self.phones:
            if str(ph) == str(new):
                edit_phone_result = True
        for ph in self.phones:
            if str(ph) == str(old) and edit_phone_result == False:
                edit_phone_result = True
                self.phones.pop(self.phones.index(ph))
                self.phones.append(Phone(new))
        if edit_phone_result == False:
            raise ValueError

    def find_phone(self, phone):

        find_phone_result = False
        for ph in self.phones:
            if str(ph) == str(phone):
                find_phone_result = True
                return ph
        if find_phone_result == False:

            return None

    def remove_phone(self, phone):

        for ph in self.phones:
            if str(ph) == str(phone):
                self.phones.pop(self.phones.index(ph))

    def __str__(self):

        res_str = ' {a1:{width}}'.format(width=20, a1=self.name.value)
        res_str += '{a2:{width}}'.format(width=30,
                                         a2='; '.join(str(p.value) for p in self.phones))
        res_str += '{a3:{width}}'.format(width=11, a3='')
        res_str += '{a4}'.format(a4=(self.birthday.value.date()
                                 if self.birthday else self.birthday))
        res_str += '{a5:{width}}'.format(width=10, a5='')
        res_str += '{a6}'.format(a6=(self.days_to_birthday()))

        return res_str

class AddressBook(UserDict):

    def add_record(self, record):
        self[record.name.value] = record

    def find(self, name):

        for nam, record in self.data.items():
            if nam == name:
                return record
            
    def find_part(self, part):
        
        ret = ''
        for nam, record in self.data.items():
            if part in nam:
                ret += str(record) + '\n'
            for ph in record.phones:
                if str(part) in str(ph):
                    ret += str(record) + '\n'
            
        return ret
                 
    def find_phone_in_book(self, phone):

        for nam, record in self.data.items():
            finded_phone = record.find_phone(phone)
            if finded_phone:
                return record
        if not finded_phone:
            return None

    def delete(self, name):

        if name in self.data:
            self.data.pop(name)


def input_error(fn):
    def inner(cmnd):

        try:
            msg = fn(cmnd)
        # except KeyError:
        #     msg = '\nSomething not good...((( Please, check HELP with "help" command.'
        except IndexError:
            msg = '\nWaiting for contact`s name and number phone.'
        except UnboundLocalError:
            msg = '\nCan`t find this contact in your pnonebook. Use "show all" to check.'
        # except ValueError:
        #     msg = '\nSomething not good...((( Please, check HELP with "help" command.'

        return msg
    return inner


@input_error
def add(cmnd):

    if cmnd[0] not in list_voc_contacts:
        voc_contact = Record(cmnd[0])
        voc_contact.add_phone(cmnd[1])
        list_voc_contacts.add_record(voc_contact)
    else:
        voc_contact = list_voc_contacts.find(cmnd[0])
        voc_contact.add_phone(cmnd[1])
    msg = f'\nIt was added for: {voc_contact.name} phone number: {cmnd[1]} in your contact`s book.'

    return msg


@input_error
def birthday(cmnd):

    if cmnd[0] not in list_voc_contacts:
        voc_contact = Record(cmnd[0])
        voc_contact.add_birthday(cmnd[1])
        list_voc_contacts.add_record(voc_contact)
    else:
        voc_contact = list_voc_contacts.find(cmnd[0])
        voc_contact.add_birthday(cmnd[1])
    msg = f'\nIt was added for: {voc_contact.name} bithday: {cmnd[1]} in your contact`s book.'

    return msg


@input_error
def change(cmnd):

    voc_contact = list_voc_contacts.find(cmnd[0])
    voc_contact.edit_phone(cmnd[1], cmnd[2])
    msg = f'\nIt was changed the phone number of: {voc_contact.name} from {cmnd[1]} on: {cmnd[2]}.'

    return msg


@input_error
def contact(cmnd):

    voc_contact = list_voc_contacts.find(cmnd[0])
    msg = f'\nI found this: {voc_contact} in my phonebook.'

    return msg


@input_error
def delete(cmnd):

    voc_contact = list_voc_contacts.find(cmnd[0])
    list_voc_contacts.delete(cmnd[0])
    msg = f'\nDeleting this contact: {voc_contact} in my phonebook.'

    return msg


def exit_bot(cmnd):

    msg = '\nGood bye! Have a nice day!'
    return msg


def find(cmnd):

    msg = f'\nWith: {cmnd[0]} I found next information in your contacts:\n'
    msg += (('-' * 100) + '\n')
    msg += (('-') + ('Name') + ('-')*18 + ('Phones') + ('-')*34 +
            ('Birthday') + ('-')*13 + ('Remain') + '-'*10 + '\n')
    msg += (('-' * 100) + '\n')
    msg += list_voc_contacts.find_part(cmnd[0])
    msg += (('-' * 100) + '\n')

    return msg


def help(cmnd):

    msg = '\nHelp for you:\n\n'
    for d1 in voc_help.items():
        msg += d1[0] + d1[1]

    return msg


def hello(cmnd):

    msg = '\nHello! How can I help you?'
    return msg


def load(cmnd):
    
    with open('book.txt', 'r') as fr:
        var_file = fr.readlines()
        for read_var in var_file:
            if (read_var[0]) == 'N':
                voc_contact = Record(read_var[1:-1])
                list_voc_contacts.add_record(voc_contact)
            elif (read_var[0]) == 'P':
                voc_contact.add_phone(read_var[1:-1])
            else:
                voc_contact.add_birthday(read_var[1:-1])
    msg = '\nYour contact`s book successfully loaded.'

    return msg


@input_error
def phone(cmnd):

    voc_contact = list_voc_contacts.find_phone_in_book(cmnd[0])
    msg = f'\nI found this: {voc_contact} in my phonebook.'

    return msg


def pr_big_msg(msg):

    c = Cust_iter()
    with open('qqq.txt', 'w') as wr:
        wr.write(msg)
    with open('qqq.txt', 'r') as rr:
        var_file = rr.readlines()
    count = 0
    while count < len(var_file):
        for _ in c:
            if _ + count <= len(var_file)-1:
                print(var_file[_ + count], end='')
            else:
                print('', end='')
        pause = input(' Please, press ENTER to continue...')
        count += _
        

@input_error
def remove(cmnd):

    voc_contact = list_voc_contacts.find_phone_in_book(cmnd[0])
    voc_contact.remove_phone(cmnd[0])
    msg = f'\nThis phone: {cmnd[0]} removed from my phonebook.'

    return msg


def save(cmnd):

    with open('book.txt', 'w') as fw:
        for name, record in list_voc_contacts.data.items():
            fw.writelines('N' + record.name.value + '\n')
            if record.phones:
                for p in record.phones:
                    fw.writelines('P' + p.value + '\n')
            if record.birthday:
                fw.writelines('B' + str(record.birthday.value.date()) + '\n')
    msg = '\nYour contact`s book successfully saved.'

    return msg


@input_error
def show_all(cmnd):

    count = 0
    msg = '\nI found next information in your contacts:\n'
    msg += (('-' * 100) + '\n')
    msg += (('-') + ('Name') + ('-')*18 + ('Phones') + ('-')*34 +
            ('Birthday') + ('-')*13 + ('Remain') + '-'*10 + '\n')
    msg += (('-' * 100) + '\n')

    for name, record in list_voc_contacts.data.items():
        msg += str(record) + '\n'

    msg += (('-' * 100) + '\n')

    return msg


def talking(cmnd):

    for pair in voc_cmnd:
        patt = re.compile('(?i)' + pair + ' ')
        s = patt.match(cmnd + ' ')
        if s != None:
            cmnd = cmnd.split()
            cmnd = deque(cmnd)
            if cmnd[0] == 'good' or cmnd[0] == 'show':
                cmnd[0] += ' ' + cmnd[1]
                voc_func = cmnd.popleft().lower()
                cmnd.popleft()
            else:
                voc_func = cmnd.popleft().lower()
            break
    if s == None:
        voc_func = 'unknown'

    return voc_cmnd[voc_func], cmnd


def unknown(cmnd):

    msg = '\nPlease, repeat... Don`t understand you.((( You can use HELP command.'
    return msg


today = datetime.today().date()
input_command = ''
list_voc_contacts = AddressBook()

voc_cmnd = {
    'add': add,
    'birthday': birthday,
    'change': change,
    'close': exit_bot,
    'contact': contact,
    'delete': delete,
    'exit': exit_bot,
    'find': find,
    'good bye': exit_bot,
    'hello': hello,
    'help': help,
    'load' : load,
    'phone': phone,
    'remove': remove,
    'save' : save,
    'show all': show_all,
    'unknown': unknown
}

voc_help = {'add': ' : add contact phone : Add contact and phone number in phonebook.\n',
            'birthday': ' birthday contact YYYY-MM-DD : Add contact`s birtday in format YYYY-MM-DD.',
            'change': ': change contact phone_old Phone_new : Change contact`s phone number on new in phonebook.\n',
            'close': ' : close : Close the bot.\n',
            'contact': ' : contact name : Display the contact`s phone.\n',
            'delete': ' : delete contact : Delete contact from phonebook.\n',
            'exit': ' : exit : Close the bot.\n',
            'find': ' : find number/name : Find contact on a part of phone number or a part of contact name.\n',
            'good bye': ' : good bye : Close the bot.\n',
            'hello': ' : hello : Greeting you))).\n',
            'help': ' : help : Display this screen with commands and parameters.\n',
            'load': ' : load : Load from disk contacts`s book',
            'phone': ' : phone number : Display the contact`s name phone owner.\n',
            'remove': ' : remove phone : Remove the phone from phonebook.',
            'save': ' : save : Save on disk contact`s book',
            'show all': ' : show all : Display your phonebook.'
            }


def main():
    while True:        
        input_command = input('\nWhat can I do for you? >>> ')
        res, cmnd = talking(input_command)
        msg = res(cmnd)
    
        if len(msg) > 800:
            pr_big_msg(msg)
        else:
            print(msg)
    
        if msg == '\nGood bye! Have a nice day!':
            exit()


if __name__ == '__main__':
    main()
