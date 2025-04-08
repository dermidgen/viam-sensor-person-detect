# Module viam-sensor-person-detect 

This sensor module offers boolean sensor detection. It assumes you're using a vision service bound to an ML model that can do people detection. Typically, you'll want to set the confidence level up pretty high on your vision service, >= 0.5.

## Model dermidgen:viam-sensor-person-detect:person-detect

Uses the camera name in conjunction with your vision service to call `get_detections_from_camera` & give back a boolean `person_detected` value from readings.

### Configuration
The following attribute template can be used to configure this model:

```json
{
"camera_name": <string,
"vision_service": <string>
}
```

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `camera_name` | string | Required  | The name of the camera you want to use |
| `vision_service` | string | Required  | The name of the vision service you've configured for detection |

#### Example Configuration

```json
{
  "camera_name": "camera-1",
  "vision_service": "vision-1"
}
```

### GetReadings

Returns boolean `person_detected` value:

```json
{
  "person_detected": <bool>
}
```

### DoCommand

Not implemented.
