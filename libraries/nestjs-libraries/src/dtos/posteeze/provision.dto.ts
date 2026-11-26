import { IsDefined, IsString, IsUUID, MaxLength, MinLength } from 'class-validator';

/** Posteeze: the Posteeze app asks for one engine workspace per customer workspace. */
export class PosteezeProvisionDto {
  @IsUUID()
  @IsDefined()
  externalId: string;

  @IsString()
  @MinLength(1)
  @MaxLength(128)
  name: string;
}
