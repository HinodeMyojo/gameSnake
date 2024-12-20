using game.Models;
using Microsoft.Extensions.Caching.Memory;
using System.Linq;
using System.Text.Json;

namespace game
{
    public class Data
    {
        private string path = "../example_response.json";  // Путь к файлу
        private IMemoryCache cache;

        public Data(IMemoryCache cache)
        {
            this.cache = cache;
        }
        public ResponseSnakeModel GetAndEdit(RequestSnakeModel? requestSnakeModel)
        {
            ResponseSnakeModel? biba = cache.Get<ResponseSnakeModel>("test");
            if (biba == null)
            {
                var obj = To();
                cache.Set("test", obj);
            }

            foreach (SnakeRequest snake in requestSnakeModel.Snakes)
            {

                Snake? snakeChose = biba!.Snakes.FirstOrDefault(x => x.Id == snake.Id);
                snakeChose.Direction = snake.Direction;
                if (biba.Food.Where(x => x.C.Contains(snakeChose.Direction)))
                {
                    snakeChose.
                }
            }


        }

        public ResponseSnakeModel To()
        {
            using FileStream fileStream = new FileStream(path, FileMode.Open);
            ResponseSnakeModel? fileJson = JsonSerializer.Deserialize<ResponseSnakeModel>(fileStream);

            return fileJson;
        }

        //ResponseSnakeModel responseSnake = new()
        //{
        //    MapSize = [180, 180, 60],
        //    Name = "IchiNiSan",
        //    Points = 0,
        //    Fences = [],
        //    Snakes = [new Snake() 
        //    {
        //        Id = new Guid("f30d89e52426486c1dd8ffe4f96361350e60cc83"),
        //        Direction = [0,0,0],
        //        OldDirection = [0,0,0],
        //        Geometry = [[101,98,26],[101,99,26]],
        //        DeathCount = 0,
        //        Status = "alive",
        //        ReviveRemainMs = 0
        //    },
        //    new Snake()
        //    {
        //        Id = new Guid("57ba0e26021920f5e8958a1379b29dc8d612dd38"),
        //        Direction = [0,0,0],
        //        OldDirection = [0,0,0],
        //        Geometry = [[64,3,57]],
        //        DeathCount = 0,
        //        Status = "alive",
        //        ReviveRemainMs = 0
        //    },
        //    new Snake()
        //    {
        //        Id = new Guid("386605993e84066a2e2418498003d3477b7c1ea1"),
        //        Direction = [0,0,0],
        //        OldDirection = [0,0,0],
        //        Geometry = [[162,71,44]],
        //        DeathCount = 0,
        //        Status = "alive",
        //        ReviveRemainMs = 0
        //    },
        //    ],
        //    Enemies
        //};
    }
}
