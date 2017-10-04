
# ============LICENSE_START==========================================
# org.onap.vvp/test-engine
# ===================================================================
# Copyright © 2017 AT&T Intellectual Property. All rights reserved.
# ===================================================================
#
# Unless otherwise specified, all software contained herein is licensed
# under the Apache License, Version 2.0 (the “License”);
# you may not use this software except in compliance with the License.
# You may obtain a copy of the License at
#
#             http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#
# Unless otherwise specified, all documentation contained herein is licensed
# under the Creative Commons License, Attribution 4.0 Intl. (the “License”);
# you may not use this documentation except in compliance with the License.
# You may obtain a copy of the License at
#
#             https://creativecommons.org/licenses/by/4.0/
#
# Unless required by applicable law or agreed to in writing, documentation
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ============LICENSE_END============================================
#
# ECOMP is a trademark and service mark of AT&T Intellectual Property.
from django.conf import settings


class ServiceProvider:
    PROGRAM_NAME = "VVP"
    MainServiceProvider = "ServiceProvider"
    email = "example.com"


class Constants:

    class FEGeneral:

        class CSS:
            H2 = 'h2'

    class Paths:

        class SSH:
            PATH = "/root/.ssh/"

        class LocalGitFolder:
            PATH = "/tmp/git_work/"

    class DBConstants:
        RETRIES_NUMBER = 120

        class Engagement:

            AIC = 'aic_instantiation_time'

        class Queries:
            COUNT = "COUNT(*)"

        class IceTables:
            NOTIFICATION = "ice_notification"
            USER_PROFILE = "ice_user_profile"
            ENGAGEMENT = "ice_engagement"
            CHECKLIST = "ice_checklist"
            RECENT = "ice_recent_engagement"
            NEXT_STEP = "ice_next_step"

    class ChecklistStates:

        class Pending:
            TEXT = "pending"

        class Automation:
            TEXT = "automation"

        class Review:
            TEXT = "review"

        class Archive:
            TEXT = "archive"

    class FEConstants:
        RETRIES_NUMBER = 120

    class GitLabConstants:
        RETRIES_NUMBER = 60

    class RGWAConstants:
        RETRIES_NUMBER = 100
        BUCKET_RETRIES_NUMBER = 180

    class ChecklistSignalsConstants:
        RETRIES_NUMBER = 10

    class Users:

        class Admin:
            EMAIL = "admin@example.com"
            FULLNAME = "admin bogus user"

        class AdminRO:
            EMAIL = "admin_ro@example.com"

        class LongEmailLengthStandardUser:
            EMAIL = "50charslengthemailofstandarduserforinvite@example.com"

    class Toast:
        ID = "toast-successfully-message"
        CMS_ID = "announcement-successfully-message"
        CSS = "html.ng-scope"

    class Cms:
        Toast_title_id = "toast-title-id"
        Toast_description = "toast-description"
        Test_addDT_close_modal_button = "close-modal-button"
        Documentation = "documentation"
        Tooltip_title = "tooltip-title"
        Tooltip_description = "tooltip-description"
        SearchDocumentation = "search-doc"
        DocumentationPageContent = ".page-content > p"

    class Template:

        class Heat:
            TEXT = "Heat Templates"

        class Subtitle:

            class SelectTemplateTitle:
                TEXT = "please-select"

    class SubmitButton:
        CSS = "button.btn.btn-primary"
        ID = "submit-modal"

    class Home:

        class Logo:
            ID = "logo"

        class Title:
            ID = "home-heading"
            TEXT = "Welcome to " + ServiceProvider.PROGRAM_NAME

        class GetStarted:
            LINK_TEXT = "Get Started"
            TEXT = "Get Started"

        class Collaborate:
            ID = "collaborate"
            XPATH = "//div[3]/div/h3"
            TEXT = "Collaborate"

        class Validate:
            XPATH = "//div[2]/div/h3"  # FIXME: change xpath
            TEXT = "Validate"

        class Incubate:
            # FIXME: change xpath
            XPATH = "//section[@id='boxes']/div/div/div/h3"
            TEXT = "Incubate"

    class Login:

        class Signup:
            LINK_TEXT = "Sign Up"

        class Title:
            CSS = "h1.ng-binding"
            TEXT = "Login"

        class SubTitle:
            CSS = "h2.ng-binding"
            TEXT = "Please use the form below to login"

        class Email:
            NAME = "email"

        class Password:
            NAME = "password"

            class Error:
                CSS = "div.form-group.has-error > div.ice-form-error > span"
                TEXT = "Password is a required field."

        class ResetPassword:
            LINK_TEXT = "Reset your password?"
            TEXT = "Reset your password?"

        class DontHaveAccount:
            ID = "id-dont-have-an-account"
            TEXT = "Don't have an account?"

        class Toast:
            TEXT = "User or Password does not match"

    class Signup:

        class Title:
            CSS = "h1.ng-binding"
            TEXT = "Sign Up"

        class SubTitle:
            CSS = "h2.ng-binding"
            TEXT = "Please use the form to Sign Up to " + \
                ServiceProvider.PROGRAM_NAME

        class Company:
            NAME = "company"

        class FullName:
            NAME = "fullname"

        class Email:
            NAME = "email"

        class Phone:
            NAME = "phone"

        class Password:
            NAME = "password"

        class RegularEmail:
            XPATH = "//input[@type='checkbox']"  # FIXME: Change XPath

        class AcceptTerms:
            XPATH = "(//input[@type='checkbox'])[2]"  # FIXME: Change XPath

        class Toast:

            class Captcha:
                TEXT = "Please fill CAPTCHA!"

            class NotMainVendor:
                TEXT = "Email address should be with service provider domain for signees that their company =" \
                       + ServiceProvider.MainServiceProvider

        class HaveAccount:
            LINK_TEXT = "Already have an account?"
            TEXT = "Already have an account?"

    class ActivateAccount:

        class Title:
            CSS = "h1.ng-binding"
            TEXT = "Activate Your Account"

        class SubTitle:
            CSS = "h2.ng-binding"
            TEXT = "Please follow the instructions below to activate your account."

        class Toast:
            TEXT = "Please activate your account first"

    class ResetPassword:

        class Toast:

            class Success:
                TEXT = "An email with detailed instructions on how to reset your password was sent to your Email."

        class Title:
            CSS = "h1.ng-binding"
            TEXT = "Reset Your Password"

        class SubTitle:
            CSS = "h2.ng-binding"
            TEXT = "Please follow the instructions below to reset your password"

        class Button:
            TEXT = "Send Instructions"

        class Email:
            NAME = "email"

    class UpdatePassword:

        class Title:
            CSS = "h1.ng-binding"
            TEXT = "Update Your Password"

        class SubTitle:
            CSS = "h2.ng-binding"
            TEXT = "Please follow the instructions below to update your password"

        class Password:
            NAME = "password"

        class ConfirmPassword:
            NAME = "confirm_password"

        class Button:
            TEXT = "Update Password"

        class Toast:
            TEXT = "Password was updated Successfully!"

    class Dashboard:

        class Modal:
            TITLE_ID = "modal-title"
            CLOSE_BUTTON_ID = "close-modal-button"

        class Default:
            DASHBOARD_ID = "dashboard"
            STATISTICS = "statistics"

        class Checklist:

            TITLE = "Checklist:"

            class ChecklistDefaultNames:
                HEAT_TEMPLATES = "Heat Templates"
                IMAGE_VALIDATION = "Image Validation"
                AIC_INSTANTIATION = "AIC Instantiation"
                ASDC_ONBOARDING = "ASDC Onboarding"

            class Name:
                ID = "cl-name-id"

            class AuditLog:
                ID = "audit-log"

                class LastLocalAuditLog:
                    CSS = "#audit-log-list > li:last-child p"

                class AuditLogList:
                    ID = "audit-log-list"

            class JenkinsLog:

                ID = "jenkins-log"

                class Modal:

                    class Title:
                        ID = "general-log-modal-title-id"
                        TEXT = "Jenkins log"

                    class Body:
                        ID = 'general-log-modal-body-id'
                        TEXT_SAMPLE = 'Started by user admin'
                        BUILD_IDENTIFIER = '/bin/sh /tmp/'

            class LineItem:

                class Approve:
                    CSS = "li.approved-cl-btn"

                class Deny:
                    CSS = "li.denied-cl-btn"

            class Approve:
                pass

            class Reject:
                ID = "state-actions-btn-reject"

                class Modal:

                    class Button:
                        ID = "reject-state"
                        TEXT = "Reject"

                    class Comment:
                        NAME = "entry_comment"

            class AddNS:
                TITLE = "Add Next Steps"
                ID = "state-actions-btn-add-next-steps"
                CSS = "span.font_header"

        class GeneralPrompt:

            class UpperTitle:
                ID = "general-prompt-upper-headline"

            class Title:
                ID = "general-prompt-title"

            class ApproveButton:
                ID = "general-prompt-approve-btn"

            class CancelButton:
                ID = "general-prompt-cancel-btn"

        class Wizard:

            class Open:
                CSS = "div[modal-animation='true']"
                CLASS_NAME = "getting-started-wizard"

            class Title:
                CSS = "h2.modal-title.ng-binding"

            class CloseButton:
                ID = "close-wizard-button"

            class AddVF:

                class Title:
                    TEXT = "Add a VF"

                class AIC_Version:
                    TEXT = "aic-version"

                class ECOMP_Release:
                    TEXT = "ecomp-release"

            class AddVendorContact:

                class Title:
                    TEXT = "Add Vendor Contact"

            class InviteTeamMembers:

                class Title:
                    NAME = "Invite Team Members"
                    TEXT = "Invite Team Members"

                class Button:
                    TEXT = "Send invitations"

            class AddSSHKey:

                class Title:
                    NAME = "Add SSH Key"
                    TEXT = "Add SSH Key"

                class TextBox:
                    NAME = "key"

        class ActivateMsg:

            class Success:
                TEXT = "You have successfully activated your account!"

            class Fail:
                TEXT = "Please activate your account first"

        class Avatar:
            ID = "avatar"

            class Account:
                LINK_TEXT = "Account"

                class Title:
                    CSS = "h2.ng-scope"
                    TEXT = "Account"

                class FullName:
                    NAME = "fullname"

                class Email:
                    NAME = "email"

                class Phone:
                    NAME = "phone"

                class Company:
                    NAME = "company"

                class SSHKey:
                    NAME = "ssh_key"

                    class UpdateFailed:
                        #                         TEXT = "Something went wrong while trying to update user account"
                        TEXT = "Updating SSH Key failed due to invalid key."

                class Update:

                    class Success:
                        TEXT = "Account was updated successfully!"

                class RGWA:

                    class Key:
                        TITLE_ID = "access-key-title"
                        KEY_ID = "access-key-value"

                    class Secret:
                        TITLE_ID = "access-secret-title"
                        SECRET_ID = "access-secret-value"
                        BUTTON_ID = "show-access-secret"
                        SECRET_TEXT = "•••••••••••••••"

                class UserProfileSettings:
                    ID = 'user-profile-settings'
                    TitleID = 'user-profile-settings-title'
                    TitleText = 'Settings'
                    ReceiveEmailsID = 'receive-emails'
                    ReceiveNotificationsID = 'receive-notifications'
                    ReceiveEmailEveryTimeID = 'receive-emails-every-time'
                    ReceiveDigestEmailID = 'receive-digest-emails'
                    UpdateButtonID = 'update-account-user-profile-settings'

            class Notifications:
                LINK_TEXT = "Notifications"

                class NotificationColumn:
                    ID = "table-col-"

                class DeleteNotification:
                    ID = "del-notification-"

                class Count:
                    ID = "notifications-count"
                    RETRIES_NUMBER = 20

                class Title:
                    ID = "notifications"
                    TEXT = "Notifications"

            class Admin:
                LINK_TEXT = "Admin"

                class Title:
                    CSS = "h1.caption"
                    TEXT = "Admin"
                    ID = "admin-toolbar-link"

            class Logout:
                LINK_TEXT = "Logout"

        class Feedback:
            ID = "feedback-toolbar-link"

            class FeedbackModal:
                SAVE_BTN_ID = "add-feedback-save-button"

        class Statuses:
            ID = "logo"

            class Body:
                ID = "search-results"
                TEXT = "Export to Excel >>"

            class Title:
                ID = "dashboard-title"
                TEXT = "Statuses"

            class FilterDropdown:
                ID = "search-filter-stage"

            class SearchBox:
                ID = "search-filter-keyword"

            class SearchFilters:
                ID = "search-filters"

            class AssignedNS:
                ID = "next-steps-header"

            class Statistics:

                class Title:
                    ID = "statistics-header"
                    TEXT = "Statistics"

                class FilterDropdown:
                    CSS = "#statistics-header > .search-filters > .search-filter-stage"

                class ValidationsNumber:
                    ID = "id-validations-num"

                class EngagementsNumber:
                    ID = "id-engagements-num"

            class News:

                class Title:
                    ID = "news-and-announcements-header"
                    TEXT = "News & Announcements"

                class List:
                    ID = "news-and-announcements-list"
                    TEXT = "There are no posts."

            class ExportExcel:
                ID = "export-to-csv"
                TEXT = "Export to Excel >>"

        class Overview:

            class AdminDropdown:
                ID = "admin-actions-dropdown"

                class ArchiveEngagement:
                    LINK_TEXT = "Archive"

                    class Wizard:

                        class Title:
                            ID = "archive-engagement-title"
                            TEXT = "Archive Engagement"

                        class Reason:
                            NAME = "reason"

                class ChangeReviewer:
                    LINK_TEXT = "Change Reviewer"

                    class Wizard:

                        class Title:
                            ID = "archive-engagement-title"
                            TEXT = "Select Engagement Lead"

                        class Select:
                            NAME = "selected-user"

                    class Toast:
                        TEXT = "Reviewer updated successfully."

                class ChangePeerReviewer:
                    LINK_TEXT = "Change Peer Reviewer"

                    class Wizard:

                        class Title:
                            ID = "archive-engagement-title"
                            TEXT = "Select Engagement Lead"

                    class Toast:
                        TEXT = "Peer reviewer updated successfully."

                class UpdateStatus:
                    LINK_TEXT = "Update Status"
                    PROGRESS = "progress"
                    PROGRESS_CSS = 'input[name="progress"]'
                    TARGET = 'vm.engagement.target_completion_date'
                    HEAT = 'vm.engagement.heat_validated_time'
                    IMAGE_SACN = 'vm.engagement.image_scan_time'
                    AIC = 'vm.engagement.aic_instantiation_time'
                    ASDC = 'vm.engagement.asdc_onboarding_time'
                    STATUS = "status"
                    SUBMIT = 'button[type="submit"]'
                    SUCCESS_MSG = 'Engagement status updated successfully.'

            class BucketURL:
                ID = "bucket-url"
                TEXT = "STORAGE BUCKET: "

            class GitURL:
                ID = "git-url"

            class Title:
                ID = "engagement-title"

            class Star:
                ID = "star-engagement-action"

            class Stage:

                class Approve:
                    XPATH = "//button[@type='submit']"  # FIXME: Change XPath

                class Deny:
                    # FIXME: Change XPath
                    XPATH = "(//button[@type='submit'])[2]"

                class Set:
                    ID = "set-stage-"

            class Progress:

                class ValidationsDates:

                    AIC_ID = 'aic-instantiation-time'
                    HEAT_ID = 'heat-validated-time'
                    IMAGE_ID = 'image-scan-time'
                    ASDC_ID = 'asdc-onboarding-time'
                    VALIDATION_DATES_ARRAY = [
                        AIC_ID, HEAT_ID, IMAGE_ID, ASDC_ID]

                class VnfVersion:
                    CLASS = "vnf_version_value"

                class Percent:
                    ID = "progress-percentage"
                    TEXT = "0 %"

                class Change:
                    ID = "edit-change-progress"
                    NUMBER = "55"
                    TEXT = "55 %"

                class Wizard:
                    NAME = "progress"

                    class Title:
                        TEXT = "Specify Progress in %"

                    class Button:
                        TEXT = "Save"

            class Status:

                class Header:
                    ID = "#engagement-status-header > span"

                class Add:
                    CSS = "i.add-engagement-status"

                class Edit:
                    CSS = "i.edit-engagement-status"

                class Description:
                    ID = "status-description"

                class LastUpdated:
                    ID = "status-update-details"

            class TeamMember:
                ID = "team-members-plus-button-id"
                MEMBER_ID = "team-member-%s"

                class Title:
                    ID = "team-member-title"

                class RemoveUser:
                    ID = "remove-member"

                    class Title:
                        TEXT = "Remove user from engagement team: %s"

                    class Message:
                        TEXT = "Are you sure you would like to remove the user out of the team members?"

            class NextSteps:

                class FilterByFileDropDown:
                    ID = "selected-file-filter-dropdown"
                    ANY_FILE_LINK_TEXT = "Any file"
                    FILE0_LINK_TEXT = "file0.yaml"
                    FILE1_LINK_TEXT = "file1.yaml"
                    FILE2_LINK_TEXT = "file2.yaml"

                class StateDropDown:
                    ID = "selected-state-filter-dropdown"
                    INCOMPLETE_LINK_TEXT = "Incomplete"
                    COMPLETED_LINK_TEXT = "Completed"

                class Add:
                    TITLE = "Engagement:"
                    ID = "add-next-step-button"

                    class Title:
                        CSS = "h2"
                        TEXT = "Add Next Steps"

                    class Description:
                        ID = "description"
                        STEP_DESC_ID = "step-description-"

                    class Button:
                        TEXT = "Submit Next Steps"

                    class AssociatedFiles:
                        ID = "associated-files-list"
                        ALL_FILES_SELECTED = "3 files selected"
                        SELECT_ALL_FILES_NAME = "Select All"

                class AssociatedFiles:
                    ID = "associated-files"
                    EmptyMsgID = "associated-files-empty-msg"
                    EmptyMsg = "There are no files for this next step"
                    FileId = "file0"

        class DetailedView:
            ID = "detailed-view-"

            class DeploymentTarget:
                ID = "deployment-targets"
                TEXT = "Deployment Targets"
                TITLE = "Add Deployment Target"
                SAVE = "add-dt-save-button"
                CSS = "span.col-md-10.ng-binding"
                ID_REMOVE_DTS = "remove-dts-"

                class AddDeploymentTargetButton:
                    ID = "add-dt"

            class VirtualFunctionComponents:
                ID = "virtual-function-components"
                TEXT = "Virtual Function Components"

            class ValidationDetails:
                PLUS = "update-validation-details"
                TITLE = "Validation Details (ECOMP, AIC, VF Version)"
                SAVE = "edit-validation-setails-save-button"
                ID = "vd-title"
                TEXT = "Validation Details"

                class TargetAICVersion:
                    ID = "target-aic-version-headline"
                    TEXT = "Target AIC Version:"
                    AIC3 = "AIC 3.0"

                class ECOMPRelease:
                    ID = "ecomp-release-headline"
                    TEXT = "ECOMP Release:"
                    ID_ECOMP = "ecomp-select-options-"
                    UNKNOW = "Unknown"

                class VFVersion:
                    ID = "vf-version-headline"
                    TEXT = "VF Version:"
                    ID_VERSION = "id-vf-version"
                    VF_VERSION_ID = "vf_version_"

            class TargetLabEntry:
                ID = "target-lab-entry"
                TEXT = "Target Lab Entry"
                CSS = "#target-lab-entry-header > span"
                CHANGE = "change-lab-entry-date"
                INPUT_CSS = '.md-datepicker-input'
                CONTENT_CSS = "h4.target-lab-entry-content"

                class Add:
                    ID = "add-dt"

            class VFC:
                TEXT = "Virtual Function Components"
                ID = "visible-dts-"

                class Add:
                    ID = "add-vfc"

                class Remove:
                    ID = "remove-vfc-"

                class Save_button:
                    ID = "add-vfc-save-button"

                class Choose_Company:
                    ID = "add-vfc-choose-company"

            class AIC:
                TEXT = "Target AIC Version"
                ID = "aic_version_"

                class Edit:
                    ID = "test_AIC_Version_Edit"

                class Confirm:
                    ID = "test_AIC_Version_Update"

                class Decline:
                    ID = "test_AIC_Version_Remove"

                class Dropdown:
                    ID = "aic-version-select"

                    class TwoPointFive:
                        ID = "aic_select_options_2.5"
                        TEXT = "2.5"

                    class Three:
                        ID = "aic_select_options_3.0"
                        TEXT = "3.0"

                    class ThreePointFive:
                        ID = "aic_select_options_3.5"
                        TEXT = "3.5"

                    class Four:
                        ID = "aic_select_options_4.0"
                        TEXT = "4.0"

                    class UniversalVersion:
                        ID = "aic_select_options_%s"

                    class NoVersion:
                        ID = "aic_select_options_No version number available"
                        TEXT = "No version number available"

            class ECOMP:
                ID = "ecomp_version_"

                class Edit:
                    ID = "test_ECOMP_Release_Edit"

                class Confirm:
                    ID = "test_ECOMP_Release_Update"

                class Decline:
                    ID = "test_ECOMP_Release_Remove"

                class Dropdown:
                    ID = "ecomp-release-select"

                    class Unknown:
                        ID = "ecomp-select-options-Unknown"

                    class UniversalRelease:
                        ID = "ecomp-select-options-%s"

        class LeftPanel:

            class Title:
                CSS = "h1.caption"
                TEXT = "Engagements"

            class AddEngagement:
                ID = "add-engagement"

            class SearchBox:
                ID = "search-eng"

                class Results:
                    ID = "search-%s"  # %s --> VF name
                    CSS = "span.search-engagement-name.ng-binding"
                    XPATH = "//input[@type='text']"

                class NoResults:
                    ID = "search-no-results"

            class CreateChecklist:
                ID = "btn-create-checklist"  # "btn-modal-update-checklist"

            class EditChecklistTemplate:
                SUCCESS_SAVE_MSG = "Template was saved successfully."
                SAVE_BTN = "Save"
                HEAT = "Editing Heat"
                SAVE_BTN_ID = "save-button"
                APPROVE_BTN_ID = "general-prompt-approve-btn"
                SUCCESS_ID = "toast-successfully-message"
                APPROVE_BTN_TITLE_ID = "general-prompt-title"
                APPROVE_BTN_TITLE_TEXT = "Are you done editing?"
                CL_TEMPLATE_SAVED_TXT = "Template was saved successfully."
                FIRST_SECTION_ID = "edit-section-btn-0"
                FIRST_SECTION_INPUT_ID = "edit-section-input-0"
                REJECT_BTN_ID = "state-actions-btn-reject"
                ADD_LINE_ITEM_BTN = "add-lineitem-btn"
                EDIT_LINE_ITEM_BTN = "edit-lineitem-btn"
                EDIT_LINE_ITEM_NAME = "edit-line-item-name-input"
                LINE_ITEM_DESC_TEXT_BOX = "edit-lineitem-description"
                EDIT_LINE_ITEM_DESC = "edit-lineitem-description-input"
                FIRST_LINE_ITEM_ID = "select-lineitem-btn-0.0"
                WYSIWYG_BUTTON_BOLD = "//button[@type='button']"
                DASHBOARD_ID = "dashboard"
                SEARCH_ENG_ID = "search-eng"
                DELETE_LINE_ITEM = "delete-lineitem-btn"

                class DefaultChecklistTemplateParametrs:
                    DEFAULT_FIRST_SECTION_VALUE = "External References"

    class EngagementStages:
        INTAKE = "Intake"
        ACTIVE = "Active"
        VALIDATED = "Validated"
        COMPLETED = "Completed"
        ALL = "All"

    class Default:

        class TestPrefix:
            Test = "test_"
            Center = "center-"

        class Password:
            TEXT = "iceusers"

            class NewPass:
                TEXT = "1234"

        class Phone:
            TEXT = "+972-50-555-5555"

        class LoginURL:
            TEXT = settings.ICE_PORTAL_URL + "/#/login"

        class DashbaordURL:
            TEXT = settings.ICE_PORTAL_URL + "/#/dashboard/dashboard"

        class OverviewURL:
            TEXT = settings.ICE_PORTAL_URL + "/#/dashboard/overview"

        class InviteURL:

            class Login:
                TEXT = settings.ICE_PORTAL_URL + "/#/login?invitation="

            class Signup:
                TEXT = settings.ICE_PORTAL_URL + "/#/signUp?eng_uuid="

        class URL:

            class Engagement:

                class EngagementOperations:
                    TEXT = settings.ICE_EM_URL + '/v1/engmgr/engagement/'

                class SingleEngagement:
                    TEXT = settings.ICE_EM_URL + \
                        '/v1/engmgr/single-engagement/'

            class Checklist:
                TEXT = settings.ICE_EM_URL + '/v1/engmgr/engagement/'

                class Get:
                    TEXT = settings.ICE_EM_URL + '/v1/engmgr/checklist/'

                class Create:
                    TEXT = settings.ICE_EM_URL + '/v1/engmgr/checklist/'

                class Update:
                    TEXT = settings.ICE_EM_URL + '/v1/engmgr/checklist/'

                class Rest:
                    TEXT = settings.EM_REST_URL + "checklist/"

            class GitLab:

                class Projects:
                    TEXT = settings.GITLAB_URL + "api/v3/projects/"

                class Users:
                    TEXT = settings.GITLAB_URL + "api/v3/users/"

        class BlockUI:
            CSS = "div.block-ui-message.ng-binding"
