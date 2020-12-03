import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'deviceName'
})
export class DeviceNamePipe implements PipeTransform {

  transform(id: string): string {
    if ("da1469x" === id) {
      return "DA1469x";
    }

    if ("da10101" === id) {
      return "DA10101";
    }

    if ("da14683" === id) {
      return "DA14682/DA14683";
    }

    if ("da14681" === id) {
      return "DA14680/DA14681";
    }

    if ("da14585" === id) {
      return "DA14585/DA14586";
    }

    if ("da14580" === id) {
      return "DA14580";
    }

    if ("da14531" === id) {
      return "DA14531";
    }

    return (id as unknown as string);
  }

}
