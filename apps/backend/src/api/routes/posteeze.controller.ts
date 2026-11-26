import {
  Body,
  Controller,
  Headers,
  HttpException,
  HttpStatus,
  Post,
} from '@nestjs/common';
import { ApiExcludeController } from '@nestjs/swagger';
import { randomBytes, timingSafeEqual } from 'crypto';
import { Provider } from '@prisma/client';
import { OrganizationService } from '@gitroom/nestjs-libraries/database/prisma/organizations/organization.service';
import { UsersService } from '@gitroom/nestjs-libraries/database/prisma/users/users.service';
import { PosteezeProvisionDto } from '@gitroom/nestjs-libraries/dtos/posteeze/provision.dto';

// Posteeze: private, server-to-server. The Posteeze app (posteeze-studio) calls
// this once per customer workspace to get its own engine organization and
// public API key. Guarded by POSTEEZE_ADMIN_KEY; disabled when it is unset.
@ApiExcludeController()
@Controller('/posteeze')
export class PosteezeController {
  constructor(
    private _orgService: OrganizationService,
    private _userService: UsersService
  ) {}

  private authorize(key?: string) {
    const expected = process.env.POSTEEZE_ADMIN_KEY || '';
    const given = Buffer.from(key || '');
    const want = Buffer.from(expected);
    if (
      expected.length < 32 ||
      given.length !== want.length ||
      !timingSafeEqual(given, want)
    ) {
      throw new HttpException('Unauthorized', HttpStatus.UNAUTHORIZED);
    }
  }

  @Post('/provision')
  async provision(
    @Headers('x-posteeze-admin') key: string,
    @Body() body: PosteezeProvisionDto
  ) {
    this.authorize(key);
    // One hidden engine user per Posteeze workspace; nobody signs in with it.
    const email = `${body.externalId}@workspaces.posteeze.com`;
    let user = await this._userService.getUserByEmail(email);
    if (!user) {
      await this._orgService.createOrgAndUser(
        {
          company: body.name.slice(0, 120),
          email,
          password: randomBytes(24).toString('hex'),
          provider: Provider.LOCAL,
        } as any,
        '0.0.0.0',
        'posteeze-studio'
      );
      user = await this._userService.getUserByEmail(email);
    }
    if (!user) {
      throw new HttpException('Provisioning failed', HttpStatus.INTERNAL_SERVER_ERROR);
    }
    const [org] = await this._orgService.getOrgsByUserId(user.id);
    if (!org) {
      throw new HttpException('Provisioning failed', HttpStatus.INTERNAL_SERVER_ERROR);
    }
    return { orgId: org.id, apiKey: org.apiKey };
  }
}
