using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace Breath_Shield.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CameraController : ControllerBase
    {
        private readonly HttpClient _httpClient;

        public CameraController(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        [HttpPost("set_raspberry_pi_ip")]
        public async Task<IActionResult> SetRaspberryPiIp([FromBody] IpAddressModel model)
        {
            var flaskUrl = $"http://{model.FlaskIp}:8080/set_camera_ip";
            var content = new StringContent(JsonSerializer.Serialize(new { camera_ip = model.RaspberryPiIp }), System.Text.Encoding.UTF8, "application/json");
            var response = await _httpClient.PostAsync(flaskUrl, content);

            if (response.IsSuccessStatusCode)
            {
                return Ok(new { status = "success" });
            }
            return BadRequest(new { status = "failure", message = "Unable to set Raspberry Pi IP" });
        }

        [HttpGet("predictions")]
        public async Task<IActionResult> GetPredictions([FromQuery] string ip)
        {
            var predictionUrl = $"http://{ip}:8080/predict";
            var response = await _httpClient.GetAsync(predictionUrl);
            if (response.IsSuccessStatusCode)
            {
                var jsonContent = await response.Content.ReadAsStringAsync();
                var predictionData = JsonSerializer.Deserialize<object>(jsonContent);
                return Ok(predictionData);
            }
            return BadRequest("Unable to retrieve predictions.");
        }
    }

    public class IpAddressModel
    {
        public string RaspberryPiIp { get; set; }
        public string FlaskIp { get; set; }
    }
}
