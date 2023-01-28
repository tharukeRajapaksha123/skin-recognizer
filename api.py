from fastapi import FastAPI, Request
import uvicorn
from pydantic import BaseModel
from skin_color_getter import detect_colors
import sqlite3


def rgb_to_hex(rgb):
    a = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
    return '%02x%02x%02x' % a


def get_items():
    try:
        conn = sqlite3.connect('geek.db')
        cursor = conn.cursor()
        data = cursor.execute('''SELECT * FROM items''')
        return data
    except Exception as e:
        print(e)
        return []


def filter_data(color_code):
    counter = 0;
    colors = []
    for code in color_code:
        color = (code['color'][0], code['color'][1], code['color'][2])
        colors.append(color)
        if counter == 1:
            break
        counter += 1
    items = get_items()
    response = []
    skin_color_codes = []
    for data in items:
        h = data[3].lstrip('#')
        code = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        for i in range(0,5):
            c = (code[0]+i,code[1]+i,code[2]+i)
            skin_color_codes.append(c)
            c = (code[0] - i, code[1] - i, code[2] - i)
            skin_color_codes.append(c)
        ids = []
        for item in items:
            color_code = item[3]
            for color in skin_color_codes:
                if color_code == rgb_to_hex(color):
                   # print(f'skin color code {rgb_to_hex(color)} {color_code}')
                    if item[0] not in ids:
                        ids.append(item[0])
                        data = {
                            "id" : item[0],
                            "name" : item[1],
                            "image_url" : item[2],
                            "description" : item[4],
                            "price" : item[5]
                        }
                        response.append(data)
    return response


class RequestBody(BaseModel):
    url: str


class Item(BaseModel):
    name: str
    image_url: str
    color_code: str
    description: str
    price: float


app = FastAPI()


@app.get("/test")
async def root():
    return {"message": "Hello World"}


@app.post("/get-skin")
async def recommend_colors(request: RequestBody):
    response = detect_colors(request.url)
    try:
        items = filter_data(response)
        return {"items": items}
    except Exception as e:
        return {"error": e}


@app.post("/save-item")
async def save_item(item: Item):
    try:
        tup = (float(item.color_code.split(",")[0]), float(item.color_code.split(",")[1]),
               float(item.color_code.split(",")[2]))
        color_code = rgb_to_hex(tup)
        query = f'''
                INSERT INTO items 
                (name,image_url,color_code,description,price)
                VALUES 
                ('{item.name}','{item.image_url}','{color_code}','{item.description}',{item.price})
            '''
        conn = sqlite3.connect('geek.db')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
        return {"message": "sucess"}
    except Exception as e:
        return {"error": e}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
