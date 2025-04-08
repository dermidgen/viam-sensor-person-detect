from typing import (Any, ClassVar, Dict, Final, List, Mapping, Optional,
                    Sequence, cast)

from typing_extensions import Self
from viam.components.sensor import *
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, ValueTypes
from viam.services.vision import Vision
from viam.components.camera import Camera


class PersonDetect(Sensor, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("dermidgen", "viam-sensor-person-detect"), "person-detect"
    )

    def __init__(self, name: str):
        super().__init__(name)
        self.camera_name = None
        self.vision_service = None

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Sensor component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any implicit dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Sequence[str]: A list of implicit dependencies
        """
        deps = []
        fields = config.attributes.fields

        # We need a camera name to pass to the detector in the vision service
        camera_name = fields.get("camera_name")
        if camera_name:
            deps.append(camera_name.string_value)
        else:
            raise ValueError("camera_name is required in the config")

        # We need the name of the vision service that provides the person detection via model
        vision_service = fields.get("vision_service")
        if vision_service:
            deps.append(vision_service.string_value)
        else:
            raise ValueError("vision_service is required in the config")


        return deps

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """

        # Set the camera name from the config
        self.camera_name = config.attributes.fields.get("camera_name").string_value

        # Let's get the vision service from the dependencies
        vision_service_name = config.attributes.fields.get("vision_service").string_value
        self.vision_service = cast(Vision, dependencies[Vision.get_resource_name(vision_service_name)])

        return super().reconfigure(config, dependencies)

    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:

        # We gotta find out from the vision service if there are any people detected
        if self.vision_service is None:
            raise ValueError("Vision service is not configured")
        try:
            
            # Let's get detections from the camera
            detections = await self.vision_service.get_detections_from_camera(self.camera_name)

        except Exception as e:
            self.logger.error(f"Error in get_readings: {e}")
            raise e
        
        return { "person_detected": 0 if not detections else 1 }

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        self.logger.error("`do_command` is not implemented")
        raise NotImplementedError()

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Geometry]:
        self.logger.error("`get_geometries` is not implemented")
        raise NotImplementedError()

