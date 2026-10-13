import { Link } from "react-router";
import { useAuth } from "../auth/AuthProvider.jsx";
import { formatPhone } from "../lib/phone.js";

// Public privacy policy (/privacy), linked from Google's consent screen.
// Written to match what the app actually does; if the app changes, update
// this page too. Have the program (and UCSB, if required) review the wording.
//
// Testing phase: this describes the trimmed app (rides keep a ride ID, not a
// name; no rider emails, notes or equipment; drivers keep a first name only).
// When the trim is lifted, rewrite the sections below to match.
const LAST_UPDATED = "October 12, 2026";

export default function Privacy() {
  const { config } = useAuth();
  const retention = config.archive_retention_days;
  const phone = config.dispatch_phone?.replace(/\D/g, "").slice(-10);
  const email = config.privacy_contact_email;

  return (
    <div className="doc-page">
      <article className="doc">
        <p className="doc-back">
          <Link to="/">← Campus Mobility Tracker</Link>
        </p>
        <h1>Privacy Policy</h1>
        <p className="muted">Last updated {LAST_UPDATED}</p>

        <p>
          Campus Mobility Tracker coordinates golf cart rides for UC Santa Barbara students who need transportation to class.
          This page explains what information the app uses, who can see it, and how long it's kept. It's a student
          project, not an official UCSB application.
        </p>
        <p>
          It covers this app only. The UCSB Mobility Program's own privacy policy also applies:{" "}
          <a href="https://mobilityprogram.sa.ucsb.edu/mtp-privacy-policy-2026" target="_blank" rel="noopener noreferrer">
            Mobility Program Privacy Policy
          </a>
          .
        </p>

        <section className="notice testing-phase" aria-labelledby="testing-phase">
          <h2 id="testing-phase">This app is in testing</h2>
          <p>
            Everything on this page describes the app <strong>during its testing phase</strong>. While it's being
            tested, it's hosted on a service that isn't yet fully approved for student information, so it
            deliberately keeps as little as possible:
          </p>
          <ul>
            <li>No rider names, email addresses, ride notes, or mobility equipment are stored.</li>
            <li>Each ride is identified by a random 6-character ride ID, and the rider's phone number is the only contact detail kept.</li>
            <li>Drivers are stored by first name only, with no phone number.</li>
          </ul>
          <p>
            If the app moves to the Mobility Program after testing, this policy will be updated before it collects
            anything more.
          </p>
        </section>

        <h2>What we collect (during testing)</h2>
        <ul>
          <li>
            <strong>Rides.</strong> For each ride: the rider's phone number, the pickup time, the pickup and drop-off
            locations, and whether it repeats weekly. Dispatch enters rides by hand or imports them from the
            program's ride request form; when importing, only those details are read, and the form's name, email,
            mobility equipment, and notes answers are skipped. Eligibility is verified separately, outside this app.
          </li>
          <li>
            <strong>Map pins (optional).</strong> Riders may mark their pickup and drop-off spots on the campus map.
          </li>
          <li>
            <strong>Ride progress.</strong> When a driver starts a ride (it's then "On the way"), when they mark it
            complete (if they do), and whether the rider confirmed they'll be there.
          </li>
          <li>
            <strong>Staff.</strong> For drivers: a first name, UCSB email address, color, weekly shift schedule, and
            how many rides they've given. For dispatchers: a UCSB email address and when they last signed in.
          </li>
          <li>
            <strong>Google sign-in.</strong> When staff or drivers sign in with Google, the app checks your email
            address and keeps only that. Google also sends your name, but it isn't stored. The app can't access your
            Gmail, Drive, contacts, calendar, or any other Google data, and it never sees your password.
          </li>
          <li>
            <strong>Driver location.</strong> Only while a driver has a ride on the way, their phone shares its GPS
            position about every 10 seconds, so the rider can see them coming. Only the most recent position is
            kept, and it's deleted once it's a day old. Location is never collected from riders.
          </li>
          <li>
            <strong>Cookies and browser storage.</strong> A sign-in cookie that keeps you signed in, a security cookie
            that protects forms, and display preferences (like hiding completed rides) saved in your own browser. No
            advertising, analytics, or tracking cookies.
          </li>
          <li>
            <strong>Server logs and rate limits.</strong> Like most websites, our hosting provider keeps standard
            server logs, such as IP addresses and the pages requested, for a limited time to run and secure the
            service. To stop abuse of the phone number lookup and sign-in, the app also briefly keeps IP addresses
            and scrambled (hashed) phone numbers, for up to an hour.
          </li>
        </ul>

        <h2>Who can see it</h2>
        <ul>
          <li>
            <strong>Dispatch staff</strong> can see all ride information, every ride's progress, and which ride each
            driver is on, with their position on the campus map.
          </li>
          <li>
            <strong>Drivers</strong> can see every ride's time, ride ID, locations, and map pins, so they can
            coordinate. Only for their own rides can they see the rider's phone number, ride link, and progress.
          </li>
          <li>
            <strong>Anyone with a ride's link</strong> can see that ride's time, locations, and map pins. From 20
            minutes before pickup (or earlier, if the driver sets off early) until the ride is over, the link also
            shows the ride's status, the driver's first name, and the driver's position on the campus map, which
            may include the end of the driver's previous ride. Links don't show the rider's phone number, and they
            stop working once the ride is over and it's 20 minutes past pickup (at most an hour after pickup).
            Please don't share your link.
          </li>
          <li>
            <strong>Phone number lookup.</strong> Entering a phone number on the home page shows the times and
            locations of that number's upcoming rides, with links to them. Lookups are rate-limited.
          </li>
          <li>
            <strong>The app's developer</strong> can see the stored information when needed to maintain and fix the
            app.
          </li>
        </ul>
        <p>
          A driver's position is only ever shown as a point on the campus map; exact GPS coordinates are never
          displayed to anyone.
        </p>

        <h2>What we don't do</h2>
        <p>
          We don't sell your information, use it for advertising, or share it with anyone outside the program, other
          than the services that run the app: our hosting provider (which stores the app and its database, in the
          United States) and Google (for sign-in).
        </p>

        <h2>How long it's kept</h2>
        <ul>
          <li>
            Rides move to an archive at 8:00 AM the morning after, and are permanently deleted once they've been
            archived for {retention} days.
          </li>
          <li>Drivers' location is deleted once it's a day old.</li>
          <li>
            This cleanup runs automatically whenever the app is in use, so over weekends and breaks, when nobody
            opens it, deletion happens the next time someone does.
          </li>
          <li>
            Your sign-in record (your email address) is kept so you can sign in again. Ask us if you'd like it
            removed.
          </li>
        </ul>

        <h2>Your choices</h2>
        <ul>
          <li>
            Drivers can decline to share location in their browser. The ride still works; the rider just won't see
            the driver on the map.
          </li>
          <li>Map pins are optional and can be changed or cleared on the ride page until the ride ends.</li>
          <li>To correct or remove your information, contact us below.</li>
        </ul>

        <h2>Contact</h2>
        <p>
          Questions about this policy or your information:{" "}
          {email && <a href={`mailto:${email}`}>{email}</a>}
          {email && phone && " or "}
          {phone && <a href={`tel:+1${phone}`}>{formatPhone(phone)}</a>}
          {!email && !phone && "contact the program's dispatch office"}.
        </p>

        <h2>Changes</h2>
        <p>
          If this policy changes, we'll update this page and the date at the top. In particular, when testing ends,
          this page will be rewritten before the app starts keeping any information it doesn't keep now.
        </p>
      </article>
    </div>
  );
}
