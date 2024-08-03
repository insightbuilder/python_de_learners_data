
#==========================================================================================
# https://stackoverflow.com/questions/12018920/wpa-handshake-with-python-hashing-difficulties
# Verify the MIC code in EAPoL Message #2 is valid, or not (WPA2)
#
#==========================================================================================
#
# The home for this code is (so check for updates):
#
#     https://www.duckware.com/tech/verify-mic-in-four-way-handshake.py.txt
#
#   and this code is fully public, as it was based on/derived from this public code:
#
#     https://stackoverflow.com/questions/12018920/wpa-handshake-with-python-hashing-difficulties
#
# 1. PMK: 'Pairwise Master Key' (256-bit) is generated from SSID/PASS in WPA2:
#
#     o https://www.wireshark.org/tools/wpa-psk.html (SSID/PASS to PMK)
#     o http://anandam.name/pbkdf2/ (Password-Based Key Derivation Function 2)
#
# 2. PRF512: The PRF-512 function is used to compute four 128-bit keys (KCK,KEK,TK1,TK2).
#    For details on this function, see:
#
#     o http://etutorials.org/Networking/802.11+security.+wi-fi+protected+access+and+802.11i/Part+II+The+Design+of+Wi-Fi+Security/Chapter+10.+WPA+and+RSN+Key+Hierarchy/Computing+the+Temporal+Keys/
#
# 3. KCK: The KCK (first 128 bits of the PTK; see above) are used to generate the MIC:
#
#     o https://tldp.org/HOWTO/8021X-HOWTO/intro.html
#
# RUN: Run the code below in an ONLINE Python 2.7 compiler.  For example:
#
#     o https://repl.it/languages/python
#     o https://www.tutorialspoint.com/execute_python_online.php
#
# CUSTOMIZE: How to customize the code below:
#
#    1) PCAP the problematic handshake (TIP: use tcpdump with ether host xx:xx:xx:xx:xx:xx)
#    2) Update SSID/PASS vars below with the known Wi-Fi name/password
#    3) Copy entire Ethernet frames for EAPoL Message #1/#2 into EAPOL1/2 vars below.
#       TIP: In Wireshark, right click on Ethernet frame, 'Copy' / '...as a Hex Stream' / paste below
#    4) Use first with a working 4-way handshake (to confirm proper usage; MIC match), then apply
#       to non-working 4-way handshake to confirm that the MIC in Message #2 is good/bad.
#    5) The code below, unmodified, results in a MIC found/calculated 'match'
#
# See also:
#
#     o https://www.wifi-professionals.com/2019/01/4-way-handshake
#     o https://stackoverflow.com/questions/15133797/creating-wpa-message-integrity-code-mic-with-python
#     o https://www.shellvoide.com/wifi/understanding-wpa-wpa2-hash-mic-cracking-process-python/
#     o https://ww.ins1gn1a.com/understanding-wpa-psk-cracking/
#     o https://docs.python.org/3/library/binascii.html
#     o https://stackoverflow.com/questions/9020843/how-to-convert-a-mac-number-to-mac-string
#
#==========================================================================================

import hmac,hashlib,binascii

def to_mac(addr): return ':'.join(addr[i:i+2] for i in range(0,len(addr),2))
def PRF_512(key,A,B): return ''.join(hmac.new(key,A+chr(0)+B+chr(i),hashlib.sha1).digest() for i in range(4))[:64]
def a2b(s): return binascii.a2b_hex(s);
def b2a(by): return binascii.b2a_hex(by);

EAPOL1 = a2b("60f189052d94a00460216606888e0203005f02008a00100000000000000001141f7a3ebdc0b51712934bef6e43ea13f80cb460f121f35408aa607046e239980000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
EAPOL2 = a2b("a0046021660660f189052d94888e0103007502010a000000000000000000015b46c7165f504c664aed90b78f3b705e02b4b029a67e3189d1632479d7e7a4e6000000000000000000000000000000000000000000000000000000000000000056de18f5efa272a4663560b73c537a65001630140100000fac040100000fac040100000fac028000")
SSID   = "your-wifi-ssid"
PASS   = "your-wifi-password"
PMK    = hashlib.pbkdf2_hmac('sha1', PASS, SSID, 4096, 32)  

VER_WPA = 2   # WPA2 means use 'SHA1'
XAUTH   = a2b("888E")
if EAPOL1[0:6]==EAPOL2[6:12] and EAPOL2[0:6]==EAPOL1[6:12] and EAPOL1[12:14]==XAUTH and EAPOL1[12:14]==XAUTH:
  if ord(EAPOL1[20])%8==VER_WPA and ord(EAPOL2[20])%8==VER_WPA:
    R1 = EAPOL1[31:63]      # random 1 (AP nonce)
    R2 = EAPOL2[31:63]      # random 2 (STA nonce)
    M1 = EAPOL2[0:6]        # MAC 1 (AP MAC)
    M2 = EAPOL1[0:6]        # MAC 2 (STA MAC)

    # Generate KCK, KEK, TK1, TK2 from the PMK (and AP/STA info)
    PTK = PRF_512(PMK,"Pairwise key expansion",min(M1,M2)+max(M1,M2)+min(R1,R2)+max(R1,R2))
    KCK = PTK[0:16];

    # try to validate the MIC in EAPoL message #2 is correct
    MICRAW   = hmac.new(KCK,EAPOL2[14:95]+a2b("00000000000000000000000000000000")+EAPOL2[111:],hashlib.sha1)
    MICFOUND = b2a(EAPOL2[95:111])
    MICCALC  = MICRAW.hexdigest()[0:32]

    print "SSID/PASS: ",SSID,"/",PASS
    print "PMK:       ",b2a(PMK)
    print "AP-MAC:    ",to_mac(b2a(M1))
    print "STA-MAC:   ",to_mac(b2a(M2))
    print "AP-NONCE:  ",b2a(R1)
    print "STA-NONCE: ",b2a(R2)
    print "KCK:       ",b2a(KCK)
    print "MIC-found: ",MICFOUND
    print "MIC-calc:  ",MICCALC
    print "Result:    ",("OK: EAPoL message #2 validated" if MICFOUND==MICCALC else "ERROR: MIC does not match")
  else:
    print "***ERROR: Did not find expected 'WPA2' version in EAPoL messages"
else:
  print "***ERROR: Problem validated Ethernet frames.  Do EAPOL1 and EAPOL2 both include the Ethernet headers?"