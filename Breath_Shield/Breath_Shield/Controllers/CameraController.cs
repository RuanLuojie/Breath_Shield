using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Threading.Tasks;
using System.Text.Json;

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

        [HttpGet("video_feed")]
        public async Task<IActionResult> GetVideoStream()
        {
            var streamUrl = "http://192.168.0.14:8080/video";
            var response = await _httpClient.GetAsync(streamUrl, HttpCompletionOption.ResponseHeadersRead);
            if (response.IsSuccessStatusCode)
            {
                var stream = await response.Content.ReadAsStreamAsync();
                return new FileStreamResult(stream, "multipart/x-mixed-replace; boundary=frame");
            }
            return BadRequest("Unable to connect to the video stream.");
        }

        // New endpoint to get prediction data
        [HttpGet("predictions")]
        public async Task<IActionResult> GetPredictions()
        {
            var predictionUrl = "http://192.168.0.14:8080/predict";
            var response = await _httpClient.GetAsync(predictionUrl);
            if (response.IsSuccessStatusCode)
            {
                // Deserialize JSON from the response
                var jsonContent = await response.Content.ReadAsStringAsync();
                var predictionData = JsonSerializer.Deserialize<object>(jsonContent);

                // Return the JSON data as is from the Flask server
                return Ok(predictionData);
            }
            return BadRequest("Unable to retrieve predictions.");
        }
    }
}
