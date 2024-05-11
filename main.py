import proxyscrape

def main():
    num_threads = int(input("How many threads do you want to use?: "))
    proxyscrape.run(num_threads)

if __name__ == "__main__":
    main()
