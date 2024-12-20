namespace game.Models
{
    public class SnakeRequest
    {
        public Guid Id { get; set; }
        public int[] Direction { get; set; } = [];
    }
}
