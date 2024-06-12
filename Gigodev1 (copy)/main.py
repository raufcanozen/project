# include <stdio.h>
# include <stdlib.h>
# include <math.h>
# include <SDL.h>
# define CURL_STATICLIB
# include <curl/curl.h>

struct
Point
{
    double
x;
double
y;
};
size_t
writeCallback(void * contents, size_t
size, size_t
nmemb, void * userp) {
    size_t
totalSize = size * nmemb;
fwrite(contents, 1, totalSize, (FILE *)
userp);
return totalSize;
}

int
main()
{
CURL * curl;
CURLcode
res;

curl = curl_easy_init();
if (curl) {

curl_easy_setopt(curl, CURLOPT_URL, "http://bilgisayar.kocaeli.edu.tr/prolab1/prolab1.txt"));

FILE * outputFile = fopen("prolab1.txt", "w");
if (outputFile) {
curl_easy_setopt(curl, CURLOPT_WRITEDATA, outputFile);
curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeCallback);


res = curl_easy_perform(curl);


curl_easy_cleanup(curl);




fclose(outputFile);

double distance(struct Point p1, struct Point p2) {
return sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y));
}


double
area(struct
Point
points[], int
n) {
double
totalArea = 0.0;
for (int i = 0; i < n - 1; i++) {
    totalArea += (points[i].x * points[i + 1].y) - (points[i + 1].x * points[i].y);
}
totalArea += (points[n - 1].x * points[0].y) - (points[0].x * points[n - 1].y);
return fabs(totalArea) / 2.0;
}

int
main()
{
enum
ShapeType
{
    TRIANGLE,
    SQUARE,
    RECTANGLE
};

int
getRandomNumber(int
min, int
max) {
return rand() % (max - min + 1) + min;
}


struct
Square
{
int
size;
int
shapeType;
};


void
drawSquare(struct
Square
square) {
for (int i = 0; i < square.size; i++) {
for (int j = 0; j < square.size; j++) {
putchar('#');
}
putchar('\n');
}
}
int
n;

printf("Nokta sayısını girin: ");
scanf("%d", & n);

struct
Point * points = (struct Point *)
malloc(n * sizeof(struct
Point));


for (int i = 0; i < n; i++) {
    printf("Nokta %d koordinatlarını girin (x y): ", i + 1);
    scanf("%lf %lf", & points[i].x, & points[i].y);
    }


    double
    totalArea = area(points, n);

    double
    resourceValue = totalArea * 10.0;

    printf("Kapalı alanın yüzey alanı: %lf\n", totalArea);
    printf("Kaynak rezerv değeri: %lf\n", resourceValue);

    # define MAX_SIZE 16
    # define MIN_SIZE 1

    enum
    ShapeType
    {
    TRIANGLE,
    SQUARE,
    RECTANGLE
    };


    int
    getRandomNumber(int
    min, int
    max) {
    return rand() % (max - min + 1) + min;
    }


    struct
    Square
    {
    int
    size;
    int
    shapeType;
    };


    void
    drawSquare(struct
    Square
    square) {
    for (int i = 0; i < square.size; i++) {
    for (int j = 0; j < square.size; j++) {
    putchar('#');
    }
    putchar('\n');
    }
    }

    void(Shape)
    {
    srand(time(NULL));

    int
    gridSize = 16;
    struct
    Square
    grid[gridSize][gridSize];

    for (int i = 0; i < gridSize; i++) {
    for (int j = 0; j < gridSize; j++) {
    grid[i][j].size = 0;
    grid[i][j].shapeType = -1;
    }
    }

    for (int i = 0; i < gridSize; i++) {
    for (int j = 0; j < gridSize; j++) {
    int size = getRandomNumber(MIN_SIZE, MAX_SIZE);
    int shapeType = getRandomNumber(0, 2);

    if (i + size <= gridSize & & j + size <= gridSize) {
    for (int x = i; x < i + size; x++) {
    for (int y = j; y < j + size; y++) {
    if (grid[x][y].size == 0) {
    grid[x][y].size = size;
    grid[x][y].shapeType = shapeType;
    }
    }
    }
    }
    }
    }

    for (int i = 0; i < gridSize; i++) {
    for (int j = 0; j < gridSize; j++) {
    if (grid[i][j].size > 0) {
    printf("Kare (%d, %d) - Boyut: %dx%d - Şekil Türü: %s\n", i, j, grid[i][j].size, grid[i][j].size,
    (grid[i][j].shapeType == TRIANGLE) ? "Üçgen": (grid[i][j].shapeType == SQUARE) ? "Kare": "Dörtgen");
    drawSquare(grid[i][j]);
    printf("\n");
    }
    }
    }

    }


    free(points);
    struct
    Surface
    {
    struct
    Point
    points[50];
    int
    pointCount;
    };

    struct
    Surface
    surfaces[50];
    int
    surfaceCount = 0;
    void
    drawScene(SDL_Renderer * renderer)
    {
    SDL_SetRenderDrawColor
    white(renderer, 255, 255, 255, 255); // Temi
