import time
import random
from multiprocessing import Process, Value, Lock

# Parent (Dear Old Dad) Process
def parent_process(bank_account, turn, lock):
    for _ in range(25):
        time.sleep(random.randint(0, 5))  # Sleep for 0-5 seconds

        with lock:
            # Wait for turn to be 0
            while turn.value != 0:
                lock.release()
                time.sleep(0.01)
                lock.acquire()

            account = bank_account.value
            if account <= 100:
                deposit = random.randint(1, 100)  # Random deposit amount between 1-100
                if deposit % 2 == 0:
                    account += deposit
                    print(f"Dear old Dad: Deposits ${deposit} / Balance = ${account}")
                else:
                    print("Dear old Dad: Doesn't have any money to give")
            else:
                print(f"Dear old Dad: Thinks Student has enough Cash (${account})")

            # Update shared variables
            bank_account.value = account
            turn.value = 1

# Child (Poor Student) Process
def child_process(bank_account, turn, lock):
    for _ in range(25):
        time.sleep(random.randint(0, 5))  # Sleep for 0-5 seconds

        with lock:
            # Wait for turn to be 1
            while turn.value != 1:
                lock.release()
                time.sleep(0.01)
                lock.acquire()

            account = bank_account.value
            withdraw = random.randint(1, 50)  # Random withdrawal amount between 1-50
            print(f"Poor Student needs ${withdraw}")
            if withdraw <= account:
                account -= withdraw
                print(f"Poor Student: Withdraws ${withdraw} / Balance = ${account}")
            else:
                print(f"Poor Student: Not Enough Cash (${account})")

            # Update shared variables
            bank_account.value = account
            turn.value = 0

# Main Function
def main():
    # Shared variables
    bank_account = Value('i', 0)  # Shared integer, initially 0
    turn = Value('i', 0)  # Shared integer for strict alternation
    lock = Lock()  # Lock for process synchronization

    # Create parent and child processes
    parent = Process(target=parent_process, args=(bank_account, turn, lock))
    child = Process(target=child_process, args=(bank_account, turn, lock))

    # Start processes
    parent.start()
    child.start()

    # Wait for both processes to complete
    parent.join()
    child.join()

    print("Simulation complete. Final balance:", bank_account.value)

if __name__ == "__main__":
    main()
