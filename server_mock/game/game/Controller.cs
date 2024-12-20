using game.Models;
using Microsoft.AspNetCore.Mvc;
using System.IO;
using System.Text.Json;

namespace game
{
    public class Controller : ControllerBase
    {
        [HttpPost("/play/snake3d/player/move")]
        public async Task<IActionResult> Move(SnakeRequest model)
        {

            return Ok();
        }
    }
}
