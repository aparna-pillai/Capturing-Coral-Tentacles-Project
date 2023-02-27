from coral_count import get_coordinates

def main():
    coordinates = get_coordinates()
    for pair in coordinates:
        print(float(pair[0]), float(pair[1]))

if __name__ == '__main__':
    main()