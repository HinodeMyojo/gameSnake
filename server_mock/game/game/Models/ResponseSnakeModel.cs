using System;

namespace game.Models
{
    public class ResponseSnakeModel
    {
        public List<int> MapSize { get; set; } = [];
        public string? Name { get; set; }
        public int Points { get; set; }
        public List<List<int>> Fences { get; set; } = [];
        public List<Snake> Snakes { get; set; } = [];
        public List<Enemy> Enemies { get; set; } = [];
        public List<Food> Food { get; set; } = [];
        public SpecialFood SpecialFood { get; set; } = [];
        public int Turn { get; set; }
        public int ReviveTimeoutSec { get; set; }
        public int TickRemainMs { get; set; }
        public List<string> Errors { get; set; } = [];
    }
    public class Snake
    {
        public Guid Id { get; set; }
        public int[] Direction { get; set; } = [];
        public List<int> OldDirection { get; set; } = [];
        public List<List<int>> Geometry { get; set; } = [];
        public int DeathCount { get; set; }
        public string? Status { get; set; }
        public int ReviveRemainMs { get; set; }
    }

    public class Enemy
    {
        public List<List<int>> Geometry { get; set; } = [];
        public string? Status { get; set; }
        public int Kills { get; set; }
    }

    public class Food
    {
        public int[] C { get; set; }
        public int Points { get; set; }
    }

    public class SpecialFood
    {
        public List<List<int>> Golden { get; set; } = [];
        public List<List<int>> Suspicious { get; set; } = [];
    }
}
