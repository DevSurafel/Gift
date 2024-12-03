import logging
import time
import random
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Replace 'YOUR_API_TOKEN' with your bot's API token
API_TOKEN = '7863411238:AAHCH7DhGTifxoiv3mpUtK4icVLcjAC6KjE'
CHAT_ID = '-1002033347065'  # Replace with your group chat ID

# List of branches and function to get a random amount
branches = ["AWASH", "OROMIA", "CBE","ABYSSINIA"]

def get_random_amount():
    return random.randint(86, 167) * 100  # Generates random amounts between 8600 and 16700, divisible by 100

# User list
user_list = [
    "Xilaahun Gamada", "Mulu Waaqjiraa", "Firaol Megersa", "Yeshi Tesfaye", "Fayyisaa Woldemichael",
"Jemila Beshir", "Abdi Guddinaa", "Tariku Daba", "Samiira Qabnaa", "Taddese Melaku",
"Waaqgari Birraa", "Rahel Girma", "Matiwos Fufa", "Ibtisaa Olani", "Genet Biruk",
"Rooba Dargii", "Mulu Bayissa", "Netsanet Demissie", "Gadaa Sabaa", "Asaffaa Jalataa",
"Meskerem Bekele", "Tafarraa Guddisaa", "Hibboo Biraanuu", "Solomon Alemayehu",
"Xinnaan Lammii", "Zahra Ali", "Waaqtolee Bulaa", "Getachew Zeleke", "Firaasaa Dirribaa",

"Tsehay Shiferaw", "Saron Fikre", "Yared Hailemariam","Morkataa Daggafaa", "Sanyii Tafarraa", "Rooba Daadhii", 
"Hana Fikadu", "Meron Birhanu", "Gammachiis Roobaa", "Sabboonaa Hordofaa", "Galanii Lammii", 
"Aaddee Bontuu", "Baayisaa Hirphasaa", "Dureessaa Iyyaasaa", 
"Dawit Yohannes", "Alemayehu Kebede", "Rahel Tsegaye", "Arfasa Gammachuu", "Fira'ol Dabalaa", "Irreechaa Abdiisaa", 
"Bereket Haile", "Selamawit Mulugeta", "Mikiyas Worku", "Galataa Haroon", "Solanaa Guddataa", "Safuu Bultii", 
"Tigist Alemu", "Yohannes Dagnachew", "Tewodros Adane", "Gannatii Dachaasaa", "Ifaa Tolasa", "Dureettii Guyyaa", 
"Fileembar Waltajjii", "Singitan Kebede", "Keebeek Sabbooqaa", "Jaallannee Mohammed", "Keebor Dastaa",
    "Kookeet Amanuel", "Kee’ol Gurmeessaa", "Hawwii Galaanaa", "Keeraaj Amantee",
    "Beekamaa Birraa", "Naafsiin Jaallataa", "Netsanet Gebremadin", "Tsagae Mokonin", "Kadija Naasir", 
    "Marsiimoy Caalaa", "Beekaa Garramuu", "Mahilet Birhanu", "Naanaat Jabeessaa", "Dinqaa Boruu", "Iftuu Bekele",
    "Biftu Jirata", "Sahil Abdul", "Firomsa Gebeyo", "Obsineet Molaatuu", "Faayaa Toleeraa", "Siinboonee Namarraa",
"Eyob Mulugeta", "Amensisa Wondwosen", "Sintayehu Wolde", "Shewaye Desta", "Lemlem Wondimu", "Wossen Tesfaye", 
"Bilisee Tolaa", "Kebede Boru", "Lalise Gabbisaa", "Dachaasaa Jaleta", "Kumsa Ayala", "Siifan Sori", "Lammii Didaa", 
"Abdiisaa Ibsa", "Dabalaa Badhaasaa", "Saba Kumsaa", "Qana'aa Gobana", "Galataa Dirribi", "Leenco Fido", 
"Mesfin Kassa", "Sintayehu Tekle", "Betelhem Bekele", "Tamrat Hailu", "Kassa Mengistu", "Mulu Birru", 
"Caalaa Teshome", "Marga Keno", "Galana Elemo", "Obsa Dinsa", "Ayantu Gudeta", "Hunde Gammadaa", 
"Yalem Taye", "Gizachew Feleke", "Habte Giorgis", "Tsion Mekuria", "Getahun Tsegaye", "Blen Kebede", "Zelalem Wolde",
"Abdisa Tufa", "Lensa Galata", "Jemal Fufa", "Bontu Geda", "Fayyisa Abebe", "Girmaa Morka", 


"Yusuf Teshome", "Nardos Kedir", "Chaltu Guddinaa", "Amir Kedir", "Gadissa Gudina",
"Aynalem Zewde", "Fayyisaa Basha", "Zamzam Tadesse", "Fizal Hordofaa", "Soreti Mekonnen",
"Abdulkerim Muktar", "Rahel Ameer", "Jemal Abarraa", "Makda Abebe", "Asayehn Waqgari",
"Sado Sora", "Biruk Qananii", "Hibbo Saanii", "Kuma Marda", "Dawit Daud",
"Mariyam Abdurrahman", "Dima Abdi", "Fawziya Fufaa", "Badhaasoo Kennaa", "Tiruneh Meles",
"Lemmi Tadesse", "Abdulaziz Beshir", "Ibtisam Hailu", "Mekdes Demissie", "Aida Gammadoo",
 "Yadessa Lammii", "Soriya Hordofaa", "Asaffaa Jaalataa", "Bilisummaa Baalu", "Mulu Mardaa",
"Nasir Kedir", "Tafara Bultum", "Samiira Daba", "Ameer Gammachuu", "Haji Abdi",
"Xilaahun Daba", "Farhia Shifa", "Ruqayya Beshir", "Getachew Lata", "Tigist Lammii",
"Jemila Abdurrahman", "Zawadi Teshome", "Fayyidaa Gurracha", "Meron Yadessa", "Diriba Gudina",
"Haile Asefa", "Fatima Basha", "Adama Waqjira", "Aster Daba", "Girma Waaqjira",
"Abiy Bultum", "Tsedale Kedir", "Amani Demissie", "Zehar Guddinaa", "Sora Abdi",
"Mulugeta Abate", "Solomon Yilma", "Tigist Habtemariam", "Amanuu Tolosaa", "Duguma Gobanaa",  
"Kaayyoo Lataa", "Dabalaa Roobaa", "Mulugeetaa Dheeressaa", "Solan Hordofaa", "Tigabu Girma", "Sahle Selassie", "Melat Yohannes", 
"Tolesaa Dabalaa", "Qananii Dheeressaa", "Obsa Waaqjiraa", "Walabummaa Tufa", "Caaltuu Daggafaa", "Alamayyoo Rorroo", 
"Sisay Girma", "Hirut Tadesse", "Beza Mengistu", "Tigabu Melaku", "Mariam Abate", "Kebede Teshome", 
"Nashida Qabena", "Sabontuu Magarsaa", "Xiyya Sabboonaa", 

 "Hunde Dinkisa", "Bedasa Abeya", "Abdisa Emiru", "Bilise Solomon", "Lali Habtamu", "Geda Jirenyaa", "Biniyam Mokonnin", "Michuu Daniel", 
    "Darartu Hambisa", "Biftu Olani", "Milkii Debala", "Musa Ebrahim", "Yosef Desale", "Samuel Tsana", "Bontu Husen", "Waggaarii Birruu", 
    "Ayantu Ijigu", "Belina Wakjira", "Yodit Tadese", "Bikiltu Oli", "Mubarek Sultan", "Ketoran Asefa", "Roba Dereje", 
    "Kulani Teshome", "Chali Debela", "Sena Bedane", "Gutama Idosa", "Lalisa Ayala", "Kenbon Taye",
    "Monet Belay","Hawi Taresa","Dachaa Ga'eera","Fata Yihun","Toofiq Likisa","Gamme Fayera","Tamirat Utura","Ferhan Ahmed",
    "Yeroosan Masqaloo", "Yordanos Beki", "Hana Markos", "Rabbirraa Wasihuun",
"Waaqjiraa Baqala", "Abarraa Bunaa", "Nagaa Eebbisaa", "Injifannoo Tasfahuun", "Malkamuu Olana",
"Fekadu Alemu", "Mahlet Ayele", "Adanech Worku", "Yonas Eshetu", "Mekonnen Teshale", "Getaneh Daba", 
"Dagmawit Terefe", "Abera Bekele", "Semira Mohammed", "Nigist Fikadu", "Tadele Haile", "Abayneh Tilahun",
"Darajjee Tolasaa", "Hirphasaa Fira'ol", "Hawwi Yadataa", "Alaaz Garoma", "Tolosaa Hunde", 
"Jirenyaa Zallaqaa", "Guddinaa Bultii", "Sirbaa Dibaabaa", "Odaa Dinquu", "Barisee Jatanii", "Guyyaa Guutamaa",  
 "Obsinet Chala", "Kennaa Jireenyaa", "Amantii Kabbadee", "Sabboontuu Olaanii", "Caaltuu Birrannaa",
     
"Lulit Wondimu", "Addis Mihretu", "Meaza Tesfaye", "Fasil Demeke", "Yared Amare", "Alem Tadesse",
    "Ibrahim Mohammed", "Ashu Bilishu", "Sena Adame", "Sisay Eshetu", "Yohanis Ebisa", "Gadise Waktole", "Natinael Bedasa", "Meti Melaku", 
    "Waadaa Ebisa", "Lalise Dhugasa", "Muhee Abduu", "Lammii Warquu", "Yadesa Regasa", "Fanose Dagi", "Sidise Ababa", "Bonsa Alamu", 
    "Carraa Bultii", "Shire Abdela", "Sudesi Shamil", "Abdi Matewos", "Chala Fufaa", "Amaddin Teha", "Thomas Wako",
    "Jirane Adisu","Abdisa Fekede","Bikila Fufa","Nagaa Jaallataa","Jaleta Sanbeta","Tabarek Abduqadir","Obsan Hordofa",
    "Seenaa Mootii", "Naahil Admasu", "Hilif Jemal","Koosaaf Amantii", "Ayishaa Mohammed", "Tolera Biyena", "Firaankoo Alemu", "Abdiikeet Wakjira", "Isaankoor Abdisa", "Abdi Olani",
    "Sington Girma","Dhugasa Tasisa","Abdeta Galma","Lami Alemayo","Obse Habtamu","Alamuddin Mahammed","Nimona Godana",
    "Geda Hirko","Kuma Sani","Simbo Tura","Mulu Sisay","Eliyas Gamechu","Fu'ad Jihad","Ebisa Kurise","Birhanu Ararsa","Sude Asrat",
    "Firrisaa Gammachuu", "Boontuu Daggafee", "Jiraannee Boggaalaa", "Moyboon Sabaa", "Tolinaa Temesgen",


"Tarikua Hailu", "Gelila Tesfaye", "Waaqo Abbaa", "Firaol Bekele", "Genet Alemayehu", "Abdi Tola", "Chaltu Dibaba",
"Lemlem Mekuria", "Jiregna Fufa", "Melat Abebe", "Biruk Kebede", "Dambii Raggaasaa", "Worke Deressa",
"Tigist Tessema", "Iyasu Bekele", "Haacaaluu Biraanuu", "Makda Girma", "Kaleb Tadesse", "Dirribaa Jaalataa",
"Yeshiwork Kassahun", "Hawi Gelan", "Wagayehu Asfaw", "Leencoo Qixxeessaa", "Hiwot Fekadu", "Ifaa Roobaa",
"Mesfin Molla", "Guddataa Gammadaa", "Zebib Alemayehu", "Gelecha Gobena", "Tigabu Mengesha", "Xilahun Tesema",
"Adaam Abarraa", "Genet Zewde", "Biyyaa Hordofaa", "Abeba Tesfaye", "Kassahun Qananii",
"Fayyisaa Aagaa", "Meseret Negash", "Asaffaa Bultum", "Gammachuu Marda", "Tigist Tessema",
"Jamila Shibru", "Hirut Demissie", "Maalim Abdi", "Lemlem Kedir", "Lammii Guyyoo",
"Tarikua Hailu", "Baayisaa Tura", "Obbo Daud", "Raafi Ramo", "Dawit Beshir",
"Birhanu Guddinaa", "Mekonnen Taye", "Sadoo Gammadaa", "Kaleb Tadesse", "Farhia Muna",
"Ruqayya Asefa", "Zewdu Mekonnen", "Dilbaro Abshiro", "Gadaa Gammachuu", "Yeshiwork Kassahun",
"Jaalala Muktar", "Gashaw Gichamo", "Biruk Kedir", "Sora Lammii", "Kuma Jiruu",
"Firaol Bekele", "Mebrak Tesfaye", "Tadessa Nagaa", "Tuujubaa Badhadha", "Armaan Fufaa",
"Badhaasoo Bichaa", "Samira Abdirahman", "Gammadaa Bultum", "Zalalem Kadir", "Firaol Basha",
"Abeera Siraj", "Tadesse Abebe", "Mekdes Kebede", "Jaalalaa Abdi", "Lalisaa Gammachuu",


"Genet Zewde", "Abeba Tesfaye", "Meseret Negash", "Asaffaa Dirribaa", "Waaqgaarii Ibsaa", "Fiixee Soraa",
"Birhanu Assefa", "Fikerte Hailu", "Zewdu Mekonnen","Xilaahun Waaqgari", "Fayyisaa Soraa", "Lammii Keno",  
"Kalkidan Yohannes", "Girma Tekle", "Kidus Tadesse", "Bilisummaa Urgeessaa", "Badhaasoo Kumsaa", "Simbirroo Qana'aa", 
"Fayyidaa Hundeessaa", "Soraa Waariyoo", "Boontuu Jifaar", "Netsanet Desta", "Mahi Shiferaw", "Hirut Demissie", 
"Gashaw Tadese", "Bethelhem Amanuel", "Eyerusalem Fekadu", "Kumaa Girmaa", "Bashannanaa Lataa", 

"Yasmin Abdurahman", "Dawit Kedir", "Safiyaa Oromia", "Tiruneh Waaqo", "Bashir Assefa",
"Fizal Teshome", "Amira Mulu", "Bilisummaa Jaalataa", "Tamirat Abebe", "Hiwot Dibaba",
"Yared Olani", "Meron Tafari", "Genet Bultum", "Fikru Shabazz", "Kassahun Hailu",
"Safiya Jimma", "Zelalem Kedir", "Soreti Abdi", "Mekdes Zewde", "Fayyidaa Dhaman",
"Yonas Gammadoo", "Biraanu Hordofaa", "Amar Kedir", "Dejen Negash", "Sanyii Teferra",
"Jemal Guracha", "Madaal Asefa", "Feyseli Balcha", "Nuru Tadesse", "Bashaan Murdar",
 "Rahel Chala", "Simeon Dibaba", "Genet Hailu", "Samiira Abarraa", "Biruk Dibaabaa",
"Fawziya Abdisa", "Mulu Teshome", "Haymanot Gammadaa", "Diriba Abdu", "Zehar Meles",
"Girma Negash", "Hana Fufa", "Kallacha Gammada", "Bilel Kedir", "Yasin Ademo",
"Biruk Jaalataa", "Amira Guracha", "Sora Qabsoo", "Fayyisaa Maammoo", "Adamu Basha",
"Abebech Zewde", "Asefa Gudina", "Chaltu Nagaa", "Mekonnen Waaqo", "Liya Amsalu",
"Aman Shiferaw", "Shamsiya Daba", "Kefyalew Tadesse", "Bontu Bultum", "Haleemaa Dima",
"Biruk Teshome", "Hana Feysel", "Nardos Tesfaye", "Gammachuu Jaalataa", "Kedir Asefa",
"Mulugeta Abebe", "Zemariam Dibaba", "Tafara Gammadoo", "Zahra Mulu", "Getachew Kebede",
"Chaltu Abarraa", "Meron Tsegaye", "Yared Kedir", "Haimanot Tesemma", "Dambalii Bulti",
"Selamawit Desta", "Jiruu Asefa", "Fiixee Negash", "Dawit Amare", "Amira Abdela",
"Tamrat Gedefa", "Nigus Marda", "Tadesse Abdi", "Bawole Damma", "Hirut Kebede",
"Mekdes Biruk", "Abebech Hailu", "Bilel Abdurrahman", "Tigist Nuru", "Gashaw Taye",
"Rashid Gammadaa", "Kaleab Teshome", "Fathiya Dabo", "Liya Mekonnen", "Enock Gebre",
"Haimanot Abebe", "Getu Bekele", "Mebratu Tadesse","Barriisaa Magarsaa", "Jirenyaa Tolasaa", 
"Liyuwork Assefa", "Tadesse Mekuria", "Aster Tsegaye","Dureettii Badhataa", "Shifarraa Lammii", "Tulluu Godaanaa", 


"Amira Waaqjira", "Seyfu Jirataa", "Nardos Abebe", "Bashir Firaol", "Ayantu Hordofaa",
"Tadesse Abdirahman", "Hana Muna", "Jemal Fufaa", "Sorbona Gammachuu", "Dawit Alama",
"Bona Tesfaye", "Waaqo Birmaduu", "Hirut Teshome", "Dira Muktar", "Fasika Olani",
"Raashiid Bultum", "Asefa Mahir", "Zalalem Sera", "Yusuf Abdissa", "Genet Meles",
"Solomon Amare", "Dawit Qananii", "Wakjira Sada", "Hawi Demissie", "Teferi Waqgari",


"Bezawit Bekele", "Abenezer Gashaw", "Rediet Getachew", "Fikadu Girma", "Mulu Abebe", "Yeshiwork Ayele", 
"Kumaa Girmaa", "Bashannanaa Lataa", "Hibboo Galgaloo", "Haimanot Abebe", "Getu Bekele", "Mebratu Tadesse", 
"Henok Berhanu", "Mekdes Tesfaye", "Habtamu Tefera", "Fitsum Workneh", "Hailu Desalegn", "Amanuel Shiferaw",



  
    "Naafiroom Wakjira", "Jennenus Olleerraa", "Alsan Eebbaa", "Fayine Garoma", "Biree Gurmuu", "Jabeessaa Dhuguma",
    "Abdii Jiraa", "Olirraa Nugusee"
]

# Function to create a transaction message for a user
def create_transaction_message(user):
    branch = random.choice(branches)
    amount = get_random_amount()
    return f"📃Transaction History:\n\nName: {user}\nBranch: {branch}\nAccount No: 1000{random.randint(1000, 9999)}********\nAmount: {amount} ETB\nTasks: Done ✅️\n\n{amount} ETB Successfully Withdrawn! ✅️"

# Prepare transaction histories with inline button
def create_transaction_histories():
    histories = []  # Fixed indentation
    for user in user_list:
        transaction = create_transaction_message(user)
        start_button = InlineKeyboardButton(text="Start", url="https://t.me/GudinaTumsaAirport_bot?start=ar3430555268")
        gift_button = InlineKeyboardButton(text="🎁 Gift", url="https://t.me/PAWSOG_bot/PAWS?startapp=tekHndQ1")
        markup = InlineKeyboardMarkup([[start_button, gift_button]])
        histories.append((transaction, markup))
    return histories

# Create a bot instance
bot = Bot(token=API_TOKEN)

# Asynchronous function to send transaction histories
async def send_transaction_histories():
    transaction_histories = create_transaction_histories()
    while True:
        for transaction, markup in transaction_histories:
            await bot.send_message(chat_id=CHAT_ID, text=transaction, reply_markup=markup)  # Use await here
            logging.info(f'Sent transaction: {transaction}')
            await asyncio.sleep(37)  # Wait for 37 seconds between each transaction message

# Main function
def main():
    logging.info("Starting the bot to send transaction histories...")
    asyncio.run(send_transaction_histories())  # Use asyncio.run to execute the async function

if __name__ == '__main__':
    main()

